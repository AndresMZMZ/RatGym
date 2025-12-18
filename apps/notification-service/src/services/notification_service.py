from typing import List
from src.models.notification_models import Notification, NotificationCreate
from src.storage.notifications_store import NotificationStore

class NotificationService:
    def __init__(self):
        self.store = NotificationStore()

    def create_notification(self, data: NotificationCreate) -> Notification:
        """Crea una nueva notificación"""
        return self.store.save(data)

    def get_notifications_by_user(self, user_id: str) -> List[Notification]:
        """Obtiene todas las notificaciones de un usuario"""
        return self.store.find_by_user(user_id)

    def get_notification_by_id(self, notification_id: str) -> Notification:
        """Obtiene una notificación por ID"""
        return self.store.find_by_id(notification_id)

    def mark_as_read(self, notification_id: str) -> bool:
        """Marca una notificación como leída"""
        return self.store.mark_as_read(notification_id)

    def delete_notification(self, notification_id: str) -> bool:
        """Elimina una notificación"""
        return self.store.delete(notification_id)

    def get_user_stats(self, user_id: str) -> dict:
        """Obtiene estadísticas de notificaciones de un usuario"""
        notifications = self.store.find_by_user(user_id)
        return {
            "total": len(notifications),
            "unread": self.store.count_unread(user_id),
            "read": len(notifications) - self.store.count_unread(user_id),
            "by_type": self._count_by_type(notifications),
            "by_priority": self._count_by_priority(notifications)
        }

    def _count_by_type(self, notifications: List[Notification]) -> dict:
        """Cuenta notificaciones por tipo"""
        counts = {}
        for n in notifications:
            counts[n.type] = counts.get(n.type, 0) + 1
        return counts

    def _count_by_priority(self, notifications: List[Notification]) -> dict:
        """Cuenta notificaciones por prioridad"""
        counts = {}
        for n in notifications:
            counts[n.priority] = counts.get(n.priority, 0) + 1
        return counts