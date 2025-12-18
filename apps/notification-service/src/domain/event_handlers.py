import json
from typing import Dict

def handle_event(event: Dict):
    """
    Punto único de entrada para eventos RabbitMQ
    """
    event_type = event.get("type")

    if event_type == "USER_CREATED":
        return {
            "user_id": event["user_id"],
            "title": "Bienvenido a RatGym",
            "message": "Tu cuenta fue creada exitosamente",
            "priority": "MEDIUM"
        }

    if event_type == "CLASS_RESERVED":
        return {
            "user_id": event["user_id"],
            "title": "Clase reservada",
            "message": f"Reservaste la clase {event.get('class_name')}",
            "priority": "HIGH"
        }

    # Evento no relevante
    return None
