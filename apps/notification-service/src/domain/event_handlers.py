import json
from typing import Dict, Optional
from datetime import datetime

def handle_event(event: Dict) -> Optional[Dict]:
    """
    Punto único de entrada para eventos RabbitMQ.
    Transforma eventos de otros microservicios en notificaciones.
    
    Returns:
        Dict con datos para crear notificación, o None si el evento no es relevante
    """
    event_type = event.get("type")
    data = event.get("data", {})
    
    # === EVENTOS DE USUARIOS ===
    if event_type == "user.created":
        return {
            "user_id": data.get("user_id"),
            "title": "¡Bienvenido a RatGym! 🎉",
            "message": f"Hola {data.get('name', 'atleta')}, tu cuenta ha sido creada exitosamente. ¡Comienza tu transformación hoy!",
            "type": "SYSTEM_INFO",
            "priority": "MEDIUM",
            "metadata": data
        }
    
    # === EVENTOS DE RUTINAS ===
    if event_type == "routine.created":
        return {
            "user_id": data.get("user_id"),
            "title": "Nueva rutina asignada 💪",
            "message": f"Se ha creado tu rutina '{data.get('routine_name', 'personalizada')}' de {data.get('duration_days', 7)} días. ¡Es hora de entrenar!",
            "type": "ROUTINE_ASSIGNED",
            "priority": "HIGH",
            "metadata": data
        }
    
    if event_type == "routine.daily_reminder":
        return {
            "user_id": data.get("user_id"),
            "title": f"Entreno del día {data.get('day_number', 1)} 🏋️",
            "message": f"Esta es tu rutina de hoy: {data.get('exercises', 'Revisa tu plan de entrenamiento')}. ¡Dale con todo!",
            "type": "DAILY_ROUTINE",
            "priority": "HIGH",
            "metadata": data
        }
    
    if event_type == "routine.completed":
        return {
            "user_id": data.get("user_id"),
            "title": "¡Entrenamiento completado! 🎖️",
            "message": f"Excelente trabajo completando tu rutina del día {data.get('day_number', '')}. Sigue así!",
            "type": "ROUTINE_COMPLETED",
            "priority": "MEDIUM",
            "metadata": data
        }
    
    if event_type == "routine.rest_day":
        return {
            "user_id": data.get("user_id"),
            "title": "Día de descanso 😴",
            "message": "Hoy es tu día de descanso. Recupérate bien para el próximo entrenamiento.",
            "type": "ROUTINE_REST",
            "priority": "LOW",
            "metadata": data
        }
    
    # === EVENTOS DE NUTRICIÓN ===
    if event_type == "nutrition.plan_created":
        return {
            "user_id": data.get("user_id"),
            "title": "Plan nutricional disponible 🥗",
            "message": f"Tu plan nutricional de {data.get('calories', '2000')} calorías está listo. ¡A comer saludable!",
            "type": "NUTRITION_PLAN",
            "priority": "HIGH",
            "metadata": data
        }
    
    if event_type == "nutrition.meal_reminder":
        return {
            "user_id": data.get("user_id"),
            "title": f"Hora de {data.get('meal_type', 'comer')} 🍽️",
            "message": f"Recuerda tu {data.get('meal_type', 'comida')}: {data.get('meal_description', 'revisa tu plan nutricional')}",
            "type": "MEAL_REMINDER",
            "priority": "MEDIUM",
            "metadata": data
        }
    
    if event_type == "nutrition.goal_achieved":
        return {
            "user_id": data.get("user_id"),
            "title": "¡Meta alcanzada! 🏆",
            "message": f"Has alcanzado tu meta de {data.get('goal_type', 'nutrición')}. ¡Felicitaciones!",
            "type": "GOAL_ACHIEVED",
            "priority": "HIGH",
            "metadata": data
        }
    
    # === EVENTOS DE CLASES ===
    if event_type == "class.scheduled":
        return {
            "user_id": data.get("user_id"),
            "title": "Clase programada 📅",
            "message": f"Tienes una clase de {data.get('class_name', 'fitness')} programada para el {data.get('date', 'próximo día')} a las {data.get('time', 'hora asignada')}",
            "type": "CLASS_REMINDER",
            "priority": "HIGH",
            "metadata": data
        }
    
    if event_type == "class.reminder":
        return {
            "user_id": data.get("user_id"),
            "title": "Recordatorio de clase ⏰",
            "message": f"Tu clase de {data.get('class_name')} comienza en {data.get('minutes_before', 30)} minutos. ¡Prepárate!",
            "type": "CLASS_REMINDER",
            "priority": "HIGH",
            "metadata": data
        }
    
    if event_type == "class.cancelled":
        return {
            "user_id": data.get("user_id"),
            "title": "Clase cancelada ❌",
            "message": f"La clase de {data.get('class_name')} ha sido cancelada. {data.get('reason', 'Consulta nuevas disponibilidades.')}",
            "type": "CLASS_CANCELLED",
            "priority": "HIGH",
            "metadata": data
        }
    
    # === EVENTOS GENERALES ===
    if event_type == "system.maintenance":
        return {
            "user_id": data.get("user_id", "all"),
            "title": "Mantenimiento del sistema 🔧",
            "message": f"El sistema estará en mantenimiento el {data.get('date', 'próximamente')}. {data.get('details', '')}",
            "type": "SYSTEM_INFO",
            "priority": "LOW",
            "metadata": data
        }
    
    # Evento no reconocido
    print(f"[!] Evento no manejado: {event_type}")
    return None

