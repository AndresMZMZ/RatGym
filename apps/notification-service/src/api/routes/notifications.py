from fastapi import APIRouter
from src.models.notification_models import NotificationCreate
from src.services.notification_service import NotificationService

router = APIRouter()
service = NotificationService()

@router.post("/", response_model=dict)
def create_notification(payload: NotificationCreate):
    return service.create_notification(payload)

@router.get("/{user_id}")
def get_user_notifications(user_id: str):
    return service.get_notifications_by_user(user_id)
