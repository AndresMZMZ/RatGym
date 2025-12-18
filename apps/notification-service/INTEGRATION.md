# 🔌 Integración con Notification Service

Guía para que otros microservicios envíen eventos al notification-service.

## 📡 Configuración de RabbitMQ

El notification-service escucha en la cola `notifications_queue` y se suscribe a los siguientes exchanges:
- `users`
- `routines`
- `nutrition`
- `classes`

## 🐍 Ejemplo en Python (FastAPI)

```python
import pika
import json
from typing import Dict

class EventPublisher:
    def __init__(self, rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"):
        self.rabbitmq_url = rabbitmq_url
    
    def publish_event(self, event_type: str, data: Dict, exchange: str = ""):
        """
        Publica un evento a RabbitMQ
        
        Args:
            event_type: Tipo de evento (ej: "routine.created")
            data: Datos del evento (debe incluir user_id)
            exchange: Exchange a usar (opcional)
        """
        try:
            connection = pika.BlockingConnection(
                pika.URLParameters(self.rabbitmq_url)
            )
            channel = connection.channel()
            
            # Declarar la cola
            channel.queue_declare(queue='notifications_queue', durable=True)
            
            # Preparar el evento
            event = {
                "type": event_type,
                "data": data
            }
            
            # Publicar
            channel.basic_publish(
                exchange=exchange,
                routing_key='notifications_queue' if not exchange else '',
                body=json.dumps(event),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistente
                )
            )
            
            print(f"✅ Evento publicado: {event_type}")
            connection.close()
            
        except Exception as e:
            print(f"❌ Error publicando evento: {e}")

# Uso en tu microservicio
publisher = EventPublisher()

# Ejemplo: Al crear una rutina
@app.post("/routines")
def create_routine(routine_data):
    # ... crear rutina en tu DB ...
    
    # Publicar evento
    publisher.publish_event(
        event_type="routine.created",
        data={
            "user_id": routine_data.user_id,
            "routine_name": routine_data.name,
            "duration_days": routine_data.duration,
            "difficulty": routine_data.difficulty
        }
    )
    
    return {"status": "created"}
```

## 📦 Ejemplo en TypeScript/Node.js (NestJS)

```typescript
import * as amqp from 'amqplib';

export class EventPublisher {
  private connection: amqp.Connection;
  private channel: amqp.Channel;

  async connect(rabbitmqUrl: string = 'amqp://guest:guest@localhost:5672/') {
    this.connection = await amqp.connect(rabbitmqUrl);
    this.channel = await this.connection.createChannel();
    await this.channel.assertQueue('notifications_queue', { durable: true });
  }

  async publishEvent(eventType: string, data: any) {
    const event = {
      type: eventType,
      data: data
    };

    this.channel.sendToQueue(
      'notifications_queue',
      Buffer.from(JSON.stringify(event)),
      { persistent: true }
    );

    console.log(`✅ Evento publicado: ${eventType}`);
  }

  async close() {
    await this.channel.close();
    await this.connection.close();
  }
}

// Uso en tu controlador
@Controller('classes')
export class ClassController {
  constructor(private eventPublisher: EventPublisher) {}

  @Post()
  async createClass(@Body() classData: CreateClassDto) {
    // ... crear clase en tu DB ...

    // Publicar evento
    await this.eventPublisher.publishEvent('class.scheduled', {
      user_id: classData.userId,
      class_name: classData.name,
      date: classData.date,
      time: classData.time
    });

    return { status: 'created' };
  }
}
```

## 📋 Eventos soportados

### 🏋️ Routine Service

```javascript
// Rutina creada
{
  "type": "routine.created",
  "data": {
    "user_id": "user123",
    "routine_name": "Full Body 7 días",
    "duration_days": 7,
    "difficulty": "intermedio"
  }
}

// Recordatorio diario
{
  "type": "routine.daily_reminder",
  "data": {
    "user_id": "user123",
    "day_number": 1,
    "routine_name": "Full Body",
    "exercises": "Sentadillas, Press banca, Dominadas"
  }
}

// Rutina completada
{
  "type": "routine.completed",
  "data": {
    "user_id": "user123",
    "day_number": 5
  }
}

// Día de descanso
{
  "type": "routine.rest_day",
  "data": {
    "user_id": "user123"
  }
}
```

### 🥗 Nutrition Service

```javascript
// Plan nutricional creado
{
  "type": "nutrition.plan_created",
  "data": {
    "user_id": "user123",
    "calories": 2500,
    "protein": 180,
    "carbs": 300,
    "fats": 70
  }
}

// Recordatorio de comida
{
  "type": "nutrition.meal_reminder",
  "data": {
    "user_id": "user123",
    "meal_type": "almuerzo",
    "meal_description": "Pollo con arroz - 500 cal"
  }
}

// Meta alcanzada
{
  "type": "nutrition.goal_achieved",
  "data": {
    "user_id": "user123",
    "goal_type": "peso objetivo"
  }
}
```

### 📅 Class Service

```javascript
// Clase programada
{
  "type": "class.scheduled",
  "data": {
    "user_id": "user123",
    "class_name": "Spinning",
    "date": "2025-12-20",
    "time": "18:00"
  }
}

// Recordatorio de clase
{
  "type": "class.reminder",
  "data": {
    "user_id": "user123",
    "class_name": "Yoga",
    "minutes_before": 30
  }
}

// Clase cancelada
{
  "type": "class.cancelled",
  "data": {
    "user_id": "user123",
    "class_name": "Pilates",
    "reason": "Instructor no disponible"
  }
}
```

### 👤 User Service

```javascript
// Usuario creado
{
  "type": "user.created",
  "data": {
    "user_id": "user123",
    "name": "Juan Pérez",
    "email": "juan@ratgym.com"
  }
}
```

## 🎯 Reglas importantes

1. **Siempre incluir `user_id`**: Todos los eventos deben tener `user_id` en los datos
2. **Formato consistente**: Usar el formato `{type, data}` 
3. **Tipos de evento**: Usar el formato `servicio.accion` (ej: `routine.created`)
4. **Datos relevantes**: Incluir toda la información necesaria para crear una notificación significativa

## 🧪 Testing

Puedes usar el script `test_events.py` incluido en el notification-service:

```bash
cd apps/notification-service
python test_events.py
```

O usar cURL para verificar notificaciones:

```bash
# Ver notificaciones de un usuario
curl http://localhost:3006/notifications/user/user123

# Ver estadísticas
curl http://localhost:3006/notifications/user/user123/stats
```

## 📊 Monitoreo

Para ver los eventos en tiempo real en RabbitMQ:
1. Abre http://localhost:15672
2. Usuario: `guest`, Password: `guest`
3. Ve a la pestaña "Queues"
4. Busca `notifications_queue`

## 🔧 Troubleshooting

**Eventos no llegan:**
- Verifica que RabbitMQ esté corriendo
- Verifica la URL de conexión
- Checa los logs del notification-service

**Notificaciones no se crean:**
- Verifica que el evento tenga `user_id`
- Verifica que el `type` esté en la lista de eventos soportados
- Revisa los logs del notification-service
