# src/storage/store.py

from src.storage.notifications_store import NotificationStore

# Singleton global del almacenamiento de notificaciones
notification_store = NotificationStore()
