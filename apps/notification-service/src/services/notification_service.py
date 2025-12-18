from src.models.notification_models import Notification, NotificationCreate
from src.storage.notifications_store import NotificationStore

class NotificationService:
    def __init__(self):
        self.store = NotificationStore()

    def create_notification(self, data: NotificationCreate) -> Notification:
        return self.store.save(data)

    def get_notifications_by_user(self, user_id: str):
        return self.store.find_by_user(user_id)