import requests
import json

# URL del servicio de notificaciones
BASE_URL = "http://localhost:3006"

# Usuario de ejemplo (usa el nombre que ingresaste en el login)
USER_ID = "camilo"  # Cambia esto por tu usuario

# Notificaciones de ejemplo variadas
sample_notifications = [
    {
        "user_id": USER_ID,
        "title": "¡Bienvenido a RatGym! 🎉",
        "message": "Tu cuenta ha sido creada exitosamente. Comienza tu transformación hoy mismo.",
        "type": "SYSTEM_INFO",
        "priority": "HIGH",
        "metadata": {"source": "onboarding"}
    },
    {
        "user_id": USER_ID,
        "title": "Nueva rutina asignada 💪",
        "message": "Tu entrenador te ha asignado una rutina de fuerza para principiantes. Incluye 4 ejercicios para todo el cuerpo.",
        "type": "ROUTINE_ASSIGNED",
        "priority": "HIGH",
        "metadata": {"routine_name": "Fuerza Principiantes", "exercises": 4}
    },
    {
        "user_id": USER_ID,
        "title": "Recordatorio de entrenamiento 📅",
        "message": "Es hora de tu sesión de piernas. ¡No te saltes el día de piernas!",
        "type": "DAILY_ROUTINE",
        "priority": "MEDIUM",
        "metadata": {"workout_type": "legs", "duration": "45 min"}
    },
    {
        "user_id": USER_ID,
        "title": "Plan nutricional listo 🥗",
        "message": "Tu plan de 2200 calorías está disponible. Incluye 150g de proteína, 250g de carbohidratos y 60g de grasas.",
        "type": "NUTRITION_PLAN",
        "priority": "HIGH",
        "metadata": {"calories": 2200, "protein": 150, "carbs": 250, "fats": 60}
    },
    {
        "user_id": USER_ID,
        "title": "Hora de almuerzo 🍽️",
        "message": "Recuerda tu comida de las 13:00. Menú sugerido: Pechuga de pollo con arroz integral y ensalada.",
        "type": "MEAL_REMINDER",
        "priority": "MEDIUM",
        "metadata": {"meal_time": "13:00", "meal_type": "almuerzo"}
    },
    {
        "user_id": USER_ID,
        "title": "Clase de yoga programada 🎯",
        "message": "Te has inscrito en la clase de Yoga Flow el viernes 20 de diciembre a las 18:00. Instructor: María García.",
        "type": "CLASS_SCHEDULED",
        "priority": "MEDIUM",
        "metadata": {"class_name": "Yoga Flow", "date": "2025-12-20", "time": "18:00", "instructor": "María García"}
    },
    {
        "user_id": USER_ID,
        "title": "Clase en 1 hora ⏰",
        "message": "Tu clase de Spinning comienza en 1 hora. Recuerda llevar tu botella de agua.",
        "type": "CLASS_REMINDER",
        "priority": "HIGH",
        "metadata": {"class_name": "Spinning", "time_remaining": "1 hour"}
    },
    {
        "user_id": USER_ID,
        "title": "¡Rutina completada! ✅",
        "message": "Completaste tu rutina de pecho y tríceps. ¡Excelente trabajo! Has quemado aproximadamente 350 calorías.",
        "type": "ROUTINE_COMPLETED",
        "priority": "LOW",
        "metadata": {"workout": "Pecho y Tríceps", "calories": 350, "duration": "55 min"}
    },
    {
        "user_id": USER_ID,
        "title": "Día de descanso 😴",
        "message": "Hoy es tu día de descanso activo. Considera hacer una caminata ligera o estiramientos.",
        "type": "REST_DAY",
        "priority": "LOW",
        "metadata": {"suggestion": "active rest"}
    },
    {
        "user_id": USER_ID,
        "title": "¡Meta alcanzada! 🏆",
        "message": "Has logrado consumir tu objetivo de proteína durante 7 días consecutivos. ¡Sigue así!",
        "type": "GOAL_ACHIEVED",
        "priority": "HIGH",
        "metadata": {"goal_type": "protein", "streak": 7}
    },
]

def create_notifications():
    print(f"🔔 Creando notificaciones de prueba para el usuario: {USER_ID}\n")
    
    success_count = 0
    error_count = 0
    
    for i, notification in enumerate(sample_notifications, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/notifications/",
                json=notification,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ [{i}/{len(sample_notifications)}] {notification['title']}")
                success_count += 1
            else:
                print(f"❌ [{i}/{len(sample_notifications)}] Error: {response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ [{i}/{len(sample_notifications)}] Error: {str(e)}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Resumen:")
    print(f"   ✅ Exitosas: {success_count}")
    print(f"   ❌ Errores: {error_count}")
    print(f"{'='*60}")
    print(f"\n🌐 Abre tu navegador en:")
    print(f"   Dashboard: http://localhost:3000")
    print(f"   Notificaciones: http://localhost:3000/notifications")
    print(f"\n💡 Pasos para probar:")
    print(f"   1. Asegúrate de haber iniciado sesión con el usuario '{USER_ID}'")
    print(f"   2. Haz clic en 'Ver más →' en el widget de Notificaciones")
    print(f"   3. Filtra por 'No leídas', 'Leídas' o 'Todas'")
    print(f"   4. Marca notificaciones como leídas o elimínalas")

if __name__ == "__main__":
    create_notifications()
