import threading
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de tu estructura de carpetas
from src.api.routes import notifications, health
# Cambiamos el nombre importado para que coincida con tu clase
from src.messaging.rabbitmq_client import RabbitMQConsumer 
from src.domain.event_handlers import handle_event

app = FastAPI(
    title="Notification Service",
    description="Microservicio de alertas y notificaciones del gimnasio",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Rutas
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    return {
        "service": "notification-service", 
        "status": "running", 
        "port": 3006
    }

# --- Lógica de RabbitMQ corregida ---

def start_rabbitmq_consumer():
    """
    Inicializa el consumidor. Usamos la clase RabbitMQConsumer que definiste.
    """
    try:
        # Instanciamos la clase con el nombre correcto
        consumer = RabbitMQConsumer()
        # Llamamos al método start() que ya definiste en ese archivo
        consumer.start()
    except Exception as e:
        print(f" [!] Error en el hilo de RabbitMQ: {e}")

@app.on_event("startup")
def startup_event():
    # Iniciamos el hilo
    thread = threading.Thread(target=start_rabbitmq_consumer, daemon=True)
    thread.start()
    print(" [*] Sistema de mensajería RabbitMQ iniciado en segundo plano.")