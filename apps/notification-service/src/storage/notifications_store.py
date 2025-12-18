import uuid
import json
import os
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv
# Asegúrate de que los nombres coincidan con src/models/notification_models.py
from src.models.notification_models import Notification, NotificationCreate

# Cargar variables de entorno
load_dotenv()

class NotificationStore:
    def __init__(self, storage_path: str = None):
        """
        Almacén de notificaciones con persistencia en JSON.
        
        Args:
            storage_path: Ruta al archivo JSON donde se guardan las notificaciones
                         Si es None, usa la variable de entorno STORAGE_PATH
        """
        if storage_path is None:
            storage_path = os.getenv("STORAGE_PATH", "data/notifications.json")
        
        self.storage_path = storage_path
        self._ensure_storage_directory()
        self._data = self._load_from_disk()

    def _ensure_storage_directory(self):
        """Crea el directorio de almacenamiento si no existe"""
        storage_dir = os.path.dirname(self.storage_path)
        if storage_dir:
            Path(storage_dir).mkdir(parents=True, exist_ok=True)

    def _load_from_disk(self) -> List[Notification]:
        """Carga notificaciones desde el archivo JSON"""
        if not os.path.exists(self.storage_path):
            return []
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Notification(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_to_disk(self):
        """Guarda todas las notificaciones al archivo JSON"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                data = [n.model_dump(mode='json') for n in self._data]
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"[!] Error guardando notificaciones: {e}")

    def save(self, data: NotificationCreate) -> Notification:
        """Crea y guarda una nueva notificación"""
        notification = Notification(
            id=str(uuid.uuid4()),
            user_id=data.user_id,
            title=data.title,
            message=data.message,
            type=data.type,
            priority=data.priority,
            read=False,
            created_at=datetime.utcnow(),
            metadata=data.metadata
        )
        self._data.append(notification)
        self._save_to_disk()
        return notification

    def find_by_user(self, user_id: str) -> List[Notification]:
        """Encuentra todas las notificaciones de un usuario"""
        return [n for n in self._data if n.user_id == user_id]

    def find_by_id(self, notification_id: str) -> Optional[Notification]:
        """Encuentra una notificación por su ID"""
        for n in self._data:
            if n.id == notification_id:
                return n
        return None

    def mark_as_read(self, notification_id: str) -> bool:
        """Marca una notificación como leída"""
        notification = self.find_by_id(notification_id)
        if notification:
            notification.read = True
            self._save_to_disk()
            return True
        return False

    def delete(self, notification_id: str) -> bool:
        """Elimina una notificación"""
        initial_length = len(self._data)
        self._data = [n for n in self._data if n.id != notification_id]
        if len(self._data) < initial_length:
            self._save_to_disk()
            return True
        return False

    def get_all(self) -> List[Notification]:
        """Obtiene todas las notificaciones"""
        return self._data

    def count_unread(self, user_id: str) -> int:
        """Cuenta notificaciones no leídas de un usuario"""
        return sum(1 for n in self._data if n.user_id == user_id and not n.read)