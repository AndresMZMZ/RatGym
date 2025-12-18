import pika
import json
import os
from dotenv import load_dotenv
# Corregimos los imports con el prefijo src.
from src.services.notification_service import NotificationService
from src.models.notification_models import NotificationCreate

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
        # Usamos el nombre de la cola del .env
        self.channel.queue_declare(queue=self.queue_name)

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_event,
            auto_ack=True
        )

        print(f" [*] Notification Service esperando eventos en la cola: {self.queue_name}")
        self.channel.start_consuming()

    def on_event(self, ch, method, properties, body):
        try:
            event = json.loads(body)
            event_type = event.get("type")
            print(f" [x] Evento recibido: {event_type}")

            if event_type == "user.created":
                self.handle_user_created(event["data"])
            elif event_type == "class.scheduled":
                self.handle_class_scheduled(event["data"])
                
        except Exception as e:
            print(f" [!] Error procesando evento: {e}")

    def handle_user_created(self, data):
        notification = NotificationCreate(
            user_id=data["user_id"],
            title="¡Bienvenido a RatGym!",
            message=f"Hola {data.get('name', '')}, tu cuenta ha sido creada correctamente.",
            type="SYSTEM_INFO",
            priority="LOW",
            metadata=data
        )
        self.service.create_notification(notification)

    def handle_class_scheduled(self, data):
        notification = NotificationCreate(
            user_id=data["user_id"],
            title="Nueva clase programada",
            message=f"Tienes una clase programada para el {data.get('date', 'próximo día')}",
            type="CLASS_REMINDER",
            priority="MEDIUM",
            metadata=data
        )
        self.service.create_notification(notification)