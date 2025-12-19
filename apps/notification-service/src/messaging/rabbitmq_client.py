import pika
import json
import os
from dotenv import load_dotenv

from src.services.notification_service import NotificationService
from src.models.notification_models import NotificationCreate
from src.domain.event_handlers import handle_event

load_dotenv()

class RabbitMQConsumer:
    def __init__(self):
        self.rabbitmq_url = os.getenv(
            "RABBITMQ_URL",
            "amqp://guest:guest@localhost:5672/"
        )
        self.queue_name = os.getenv(
            "NOTIFICATIONS_QUEUE",
            "notifications_queue"
        )

        params = pika.URLParameters(self.rabbitmq_url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # IMPORTANTE: el service ya usa el singleton internamente
        self.service = NotificationService()

    def start(self):
        self.channel.queue_declare(queue=self.queue_name, durable=False)

        exchanges = ['users', 'routines', 'nutrition', 'classes']
        for exchange in exchanges:
            self.channel.exchange_declare(
                exchange=exchange,
                exchange_type='topic',
                durable=False
            )
            self.channel.queue_bind(
                exchange=exchange,
                queue=self.queue_name,
                routing_key='#'
            )
            print(f" [✓] Suscrito al exchange: {exchange}")

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_event,
            auto_ack=True
        )

        print(f" [*] Notification Service esperando eventos en la cola: {self.queue_name}")
        print(f" [*] Escuchando exchanges: {', '.join(exchanges)}")
        self.channel.start_consuming()

    def on_event(self, ch, method, properties, body):
        try:
            event = json.loads(body)
            event_type = event.get("type")
            print(f" [x] Evento recibido: {event_type}")

            notification_data = handle_event(event)

            if notification_data:
                notification = NotificationCreate(**notification_data)
                created = self.service.create_notification(notification)
                print(
                    f" [✓] Notificación creada: {created.id} "
                    f"para usuario {created.user_id}"
                )
            else:
                print(f" [!] Evento {event_type} no generó notificación")

        except Exception as e:
            print(f" [!] Error procesando evento: {e}")
            import traceback
            traceback.print_exc()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print(" [x] Conexión a RabbitMQ cerrada")
