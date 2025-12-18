import uuid
from datetime import datetime
# Asegúrate de que los nombres coincidan con src/models/notification_models.py
from src.models.notification_models import Notification, NotificationCreate

class NotificationStore:
    def __init__(self):
        self._data = []

    def save(self, data: NotificationCreate) -> Notification:
        # Usamos los nombres exactos que definiste en el modelo Notification
        notification = Notification(
            id=str(uuid.uuid4()),      # Antes tenías notification_id
            user_id=data.user_id,
            title=data.title,
            message=data.message,
            type=data.type,
            priority=data.priority,
            read=False,                # Antes tenías is_read
            created_at=datetime.utcnow(),
            metadata=data.metadata
        )
        self._data.append(notification)
        return notification

    def find_by_user(self, user_id: str):
        return [n for n in self._data if n.user_id == user_id]