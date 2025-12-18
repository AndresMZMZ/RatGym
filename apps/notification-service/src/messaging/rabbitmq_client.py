import pika
import json
import os
from dotenv import load_dotenv
# Corregimos los imports con el prefijo src.
from src.services.notification_service import NotificationService
from src.models.notification_models import NotificationCreate
from src.domain.event_handlers import handle_event

# Cargamos las variables de entorno
load_dotenv()

class RabbitMQConsumer:
    def __init__(self):
        # Obtenemos la URL y la cola desde el .env
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.queue_name = os.getenv("NOTIFICATIONS_QUEUE", "notifications_queue")
        
        # Conexión usando la URL del .env
        params = pika.URLParameters(self.rabbitmq_url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.service = NotificationService()

    def start(self):
        # Declaramos la cola principal
        self.channel.queue_declare(queue=self.queue_name, durable=False)
        
        # También podemos suscribirnos a exchanges específicos para diferentes tipos de eventos
        exchanges = ['users', 'routines', 'nutrition', 'classes']
        for exchange in exchanges:
            try:
                self.channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=False)
                # Binding de la cola a cada exchange con pattern #
                self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key='#')
                print(f" [✓] Suscrito al exchange: {exchange}")
            except Exception as e:
                print(f" [!] No se pudo suscribir al exchange {exchange}: {e}")

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_event,
            auto_ack=True
        )

        print(f" [*] Notification Service esperando eventos en la cola: {self.queue_name}")
        print(f" [*] Escuchando exchanges: {', '.join(exchanges)}")
        self.channel.start_consuming()

    def on_event(self, ch, method, properties, body):
        """
        Callback que se ejecuta cuando llega un evento.
        Usa el event_handler para procesar el evento de forma desacoplada.
        """
        try:
            event = json.loads(body)
            event_type = event.get("type")
            print(f" [x] Evento recibido: {event_type}")

            # Usamos el handler desacoplado del dominio
            notification_data = handle_event(event)
            
            if notification_data:
                # Creamos la notificación usando el servicio
                notification = NotificationCreate(**notification_data)
                created = self.service.create_notification(notification)
                print(f" [✓] Notificación creada: {created.id} para usuario {created.user_id}")
            else:
                print(f" [!] Evento {event_type} no generó notificación")
                
        except json.JSONDecodeError as e:
            print(f" [!] Error decodificando JSON: {e}")
        except Exception as e:
            print(f" [!] Error procesando evento: {e}")
            import traceback
            traceback.print_exc()

    def close(self):
        """Cierra la conexión limpiamente"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print(" [x] Conexión a RabbitMQ cerrada")