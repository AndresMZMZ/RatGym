# 📬 Notification Service - RatGym

Microservicio de notificaciones para la plataforma RatGym. Gestiona alertas y mensajes personalizados basados en eventos de otros microservicios (rutinas, nutrición, clases).

## 🎯 Características

- ✅ **Persistencia local**: Almacenamiento en JSON con volumen persistente
- ✅ **Mensajería asíncrona**: Consumo de eventos RabbitMQ
- ✅ **API REST completa**: CRUD de notificaciones
- ✅ **Notificaciones inteligentes**: Basadas en eventos de rutinas, nutrición y clases
- ✅ **Estadísticas**: Contador de notificaciones leídas/no leídas por tipo y prioridad

## 🚀 Cómo correr localmente

### 1. Instalar dependencias

```bash
cd apps/notification-service
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia `.env.example` a `.env` y ajusta los valores:

```bash
cp .env.example .env
```

Variables principales:
- `PORT=3006` - Puerto del servicio
- `RABBITMQ_URL=amqp://guest:guest@localhost:5672/` - URL de RabbitMQ
- `STORAGE_PATH=data/notifications.json` - Ruta del archivo de persistencia

### 3. Ejecutar el servicio

```bash
# Desde la raíz del microservicio
uvicorn src.main:app --host 0.0.0.0 --port 3006 --reload
```

El servicio estará disponible en: **http://localhost:3006**

## 📡 Endpoints disponibles

### Health Check
- `GET /health` - Verifica el estado del servicio

### Notificaciones

#### Obtener notificaciones de un usuario
```http
GET /notifications/user/{user_id}
```
Retorna todas las notificaciones del usuario.

#### Obtener estadísticas de un usuario
```http
GET /notifications/user/{user_id}/stats
```
Retorna contadores y estadísticas:
```json
{
  "total": 10,
  "unread": 3,
  "read": 7,
  "by_type": {
    "ROUTINE_ASSIGNED": 2,
    "DAILY_ROUTINE": 5,
    "NUTRITION_PLAN": 3
  },
  "by_priority": {
    "HIGH": 5,
    "MEDIUM": 3,
    "LOW": 2
  }
}
```

#### Obtener una notificación específica
```http
GET /notifications/{notification_id}
```

#### Marcar como leída
```http
PATCH /notifications/{notification_id}/read
```

#### Eliminar notificación
```http
DELETE /notifications/{notification_id}
```

#### Crear notificación manual
```http
POST /notifications/
Content-Type: application/json

{
  "user_id": "user123",
  "title": "Título de la notificación",
  "message": "Mensaje personalizado",
  "type": "SYSTEM_INFO",
  "priority": "MEDIUM",
  "metadata": {}
}
```

## 📨 Eventos que consume

El servicio escucha eventos de RabbitMQ en los siguientes exchanges:

### 🏋️ Eventos de Rutinas (`routines` exchange)
- `routine.created` - Nueva rutina asignada
- `routine.daily_reminder` - Recordatorio diario de entrenamiento
- `routine.completed` - Rutina completada
- `routine.rest_day` - Día de descanso

### 🥗 Eventos de Nutrición (`nutrition` exchange)
- `nutrition.plan_created` - Plan nutricional creado
- `nutrition.meal_reminder` - Recordatorio de comida
- `nutrition.goal_achieved` - Meta nutricional alcanzada

### 📅 Eventos de Clases (`classes` exchange)
- `class.scheduled` - Clase programada
- `class.reminder` - Recordatorio de clase próxima
- `class.cancelled` - Clase cancelada

### 👤 Eventos de Usuarios (`users` exchange)
- `user.created` - Nuevo usuario registrado

### Formato de evento
```json
{
  "type": "routine.daily_reminder",
  "data": {
    "user_id": "user123",
    "routine_name": "Rutina Full Body",
    "day_number": 3,
    "exercises": "Sentadillas, Press de banca, Peso muerto"
  }
}
```

## 🐳 Docker

### Construir imagen
```bash
docker build -t notification-service:latest .
```

### Ejecutar contenedor
```bash
docker run -p 3006:3006 \
  -e RABBITMQ_URL=amqp://guest:guest@host.docker.internal:5672/ \
  -v $(pwd)/data:/app/data \
  notification-service:latest
```

## ☸️ Kubernetes

### Desplegar en cluster
```bash
kubectl apply -f ../../infra/k8s/deployments/notification-service.yaml
```

### Port forward para acceso local
```bash
kubectl port-forward svc/notification-service 3006:3006
```

## 📁 Estructura del proyecto

```
notification-service/
├── src/
│   ├── main.py                    # Punto de entrada FastAPI
│   ├── api/
│   │   └── routes/
│   │       ├── notifications.py   # Endpoints REST
│   │       └── health.py          # Health check
│   ├── domain/
│   │   └── event_handlers.py      # Procesamiento de eventos
│   ├── messaging/
│   │   └── rabbitmq_client.py     # Cliente RabbitMQ
│   ├── models/
│   │   └── notification_models.py # Modelos Pydantic
│   ├── services/
│   │   └── notification_service.py # Lógica de negocio
│   └── storage/
│       └── notifications_store.py  # Persistencia JSON
├── data/                           # Almacenamiento local (gitignore)
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 🔒 Tipos de notificaciones

- `SYSTEM_INFO` - Información del sistema
- `ROUTINE_ASSIGNED` - Rutina asignada
- `DAILY_ROUTINE` - Rutina del día
- `ROUTINE_COMPLETED` - Rutina completada
- `ROUTINE_REST` - Día de descanso
- `NUTRITION_PLAN` - Plan nutricional
- `MEAL_REMINDER` - Recordatorio de comida
- `GOAL_ACHIEVED` - Meta alcanzada
- `CLASS_REMINDER` - Recordatorio de clase
- `CLASS_CANCELLED` - Clase cancelada

## ⚡ Prioridades

- `HIGH` - Urgente, requiere atención inmediata
- `MEDIUM` - Normal
- `LOW` - Informativa

## 🧪 Testing

```bash
# Crear notificación de prueba
curl -X POST http://localhost:3006/notifications/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "title": "Test",
    "message": "Mensaje de prueba",
    "type": "SYSTEM_INFO",
    "priority": "LOW"
  }'

# Obtener notificaciones
curl http://localhost:3006/notifications/user/test_user

# Estadísticas
curl http://localhost:3006/notifications/user/test_user/stats
```

## 📝 Notas importantes

- Las notificaciones se guardan en `data/notifications.json` por defecto
- El volumen debe montarse correctamente en K8s para persistencia
- RabbitMQ debe estar corriendo antes de iniciar el servicio
- El servicio se conecta automáticamente a los exchanges al iniciar

## 🔧 Troubleshooting

**Error de conexión a RabbitMQ:**
```bash
# Verificar que RabbitMQ esté corriendo
kubectl get pods | grep rabbitmq
# O localmente
docker ps | grep rabbitmq
```

**Archivo de datos no se crea:**
```bash
# Crear directorio manualmente
mkdir -p data
# Verificar permisos
chmod 755 data
```

## 👥 Integración con otros servicios

Este microservicio está diseñado para trabajar con:
- **user-service** (puerto 3001) - Eventos de usuarios
- **routine-service** - Eventos de rutinas
- **nutrition-service** - Eventos de nutrición  
- **class-service** - Eventos de clases
- **shell** (frontend) - Consumo de notificaciones

---

**Puerto:** 3006  
**Versión:** 1.0.0  
**Arquitectura:** Saga con coreografía