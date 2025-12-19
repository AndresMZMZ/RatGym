from typing import List
from src.models.notification_models import Notification, NotificationCreate
from src.storage.store import notification_store


class NotificationService:
    def __init__(self):
        # USAMOS EL SINGLETON
        self.store = notification_store

    def create_notification(self, data: NotificationCreate) -> Notification:
        return self.store.save(data)

    def get_notifications_by_user(self, user_id: str) -> List[Notification]:
        return self.store.find_by_user(user_id)

    def get_notification_by_id(self, notification_id: str) -> Notification:
        return self.store.find_by_id(notification_id)

    def mark_as_read(self, notification_id: str) -> bool:
        return self.store.mark_as_read(notification_id)

    def delete_notification(self, notification_id: str) -> bool:
        return self.store.delete(notification_id)

    def get_user_stats(self, user_id: str) -> dict:
        notifications = self.store.find_by_user(user_id)
        unread = self.store.count_unread(user_id)

        return {
            "total": len(notifications),
            "unread": unread,
            "read": len(notifications) - unread,
            "by_type": self._count_by_type(notifications),
            "by_priority": self._count_by_priority(notifications)
        }

    def _count_by_type(self, notifications: List[Notification]) -> dict:
        counts = {}
        for n in notifications:
            counts[n.type] = counts.get(n.type, 0) + 1
        return counts

    def _count_by_priority(self, notifications: List[Notification]) -> dict:
        counts = {}
        for n in notifications:
            counts[n.priority] = counts.get(n.priority, 0) + 1
        return counts
