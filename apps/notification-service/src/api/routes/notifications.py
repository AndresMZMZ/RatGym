from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.notification_models import NotificationCreate, Notification
from src.services.notification_service import NotificationService

router = APIRouter()
service = NotificationService()

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
def create_notification(payload: NotificationCreate):
    """
    Crea una nueva notificación manualmente.
    Normalmente las notificaciones se crean automáticamente por eventos.
    """
    return service.create_notification(payload)

@router.get("/user/{user_id}", response_model=List[Notification])
def get_user_notifications(user_id: str):
    """
    Obtiene todas las notificaciones de un usuario.
    """
    notifications = service.get_notifications_by_user(user_id)
    return notifications

@router.get("/user/{user_id}/stats", response_model=dict)
def get_user_stats(user_id: str):
    """
    Obtiene estadísticas de notificaciones de un usuario.
    """
    return service.get_user_stats(user_id)

@router.get("/{notification_id}", response_model=Notification)
def get_notification(notification_id: str):
    """
    Obtiene una notificación específica por su ID.
    """
    notification = service.get_notification_by_id(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notificación {notification_id} no encontrada"
        )
    return notification

@router.patch("/{notification_id}/read", response_model=dict)
def mark_notification_as_read(notification_id: str):
    """
    Marca una notificación como leída.
    """
    success = service.mark_as_read(notification_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notificación {notification_id} no encontrada"
        )
    return {"message": "Notificación marcada como leída", "id": notification_id}

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: str):
    """
    Elimina una notificación.
    """
    success = service.delete_notification(notification_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notificación {notification_id} no encontrada"
        )
    return None

