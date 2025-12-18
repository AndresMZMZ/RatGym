"""
Script de prueba para enviar eventos al Notification Service
Simula eventos de otros microservicios
"""
import pika
import json
import sys

def send_event(event_type, data):
    """Envía un evento a RabbitMQ"""
    try:
        # Conectar a RabbitMQ
        connection = pika.BlockingConnection(
            pika.URLParameters('amqp://guest:guest@localhost:5672/')
        )
        channel = connection.channel()
        
        # Declarar la cola (debe coincidir con la configuración existente)
        channel.queue_declare(queue='notifications_queue', durable=False)
        
        # Preparar el evento
        event = {
            "type": event_type,
            "data": data
        }
        
        # Enviar mensaje
        channel.basic_publish(
            exchange='',
            routing_key='notifications_queue',
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=1,  # Non-persistent (para cola no durable)
            )
        )
        
        print(f"✅ Evento enviado: {event_type}")
        print(f"   Datos: {json.dumps(data, indent=2)}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error enviando evento: {e}")
        return False

def main():
    print("🧪 Script de prueba - Notification Service\n")
    
    # Ejemplo 1: Usuario creado
    print("1️⃣ Enviando evento: user.created")
    send_event("user.created", {
        "user_id": "user_123",
        "name": "Juan Pérez",
        "email": "juan@ratgym.com"
    })
    
    # Ejemplo 2: Rutina creada
    print("\n2️⃣ Enviando evento: routine.created")
    send_event("routine.created", {
        "user_id": "user_123",
        "routine_name": "Full Body 7 días",
        "duration_days": 7,
        "difficulty": "intermedio"
    })
    
    # Ejemplo 3: Recordatorio diario de rutina
    print("\n3️⃣ Enviando evento: routine.daily_reminder")
    send_event("routine.daily_reminder", {
        "user_id": "user_123",
        "day_number": 1,
        "routine_name": "Full Body",
        "exercises": "Sentadillas 4x12, Press banca 4x10, Dominadas 3x8"
    })
    
    # Ejemplo 4: Plan nutricional creado
    print("\n4️⃣ Enviando evento: nutrition.plan_created")
    send_event("nutrition.plan_created", {
        "user_id": "user_123",
        "calories": 2500,
        "protein": 180,
        "carbs": 300,
        "fats": 70
    })
    
    # Ejemplo 5: Recordatorio de comida
    print("\n5️⃣ Enviando evento: nutrition.meal_reminder")
    send_event("nutrition.meal_reminder", {
        "user_id": "user_123",
        "meal_type": "almuerzo",
        "meal_description": "Pollo con arroz y vegetales - 500 cal"
    })
    
    # Ejemplo 6: Clase programada
    print("\n6️⃣ Enviando evento: class.scheduled")
    send_event("class.scheduled", {
        "user_id": "user_123",
        "class_name": "Spinning",
        "date": "2025-12-20",
        "time": "18:00"
    })
    
    print("\n✅ Todos los eventos de prueba fueron enviados")
    print("📬 Verifica las notificaciones en: http://localhost:3006/notifications/user/user_123")

if __name__ == "__main__":
    main()
