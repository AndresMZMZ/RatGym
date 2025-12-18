import threading
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Cargar variables de entorno
load_dotenv()

# Importaciones de tu estructura de carpetas
from src.api.routes import notifications, health
# Cambiamos el nombre importado para que coincida con tu clase
from src.messaging.rabbitmq_client import RabbitMQConsumer 

app = FastAPI(
    title="Notification Service",
    description="Microservicio de alertas y notificaciones del gimnasio RatGym",
    version="1.0.0"
)

# Configuración de CORS desde .env
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
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
        "port": int(os.getenv("PORT", 3006)),
        "version": "1.0.0"
    }

# --- Lógica de RabbitMQ ---

def start_rabbitmq_consumer():
    """
    Inicializa el consumidor de RabbitMQ en un hilo separado.
    """
    try:
        consumer = RabbitMQConsumer()
        consumer.start()
    except Exception as e:
        print(f" [!] Error en el hilo de RabbitMQ: {e}")
        import traceback
        traceback.print_exc()

@app.on_event("startup")
def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    print(" [*] Iniciando Notification Service...")
    print(f" [*] Puerto: {os.getenv('PORT', 3006)}")
    print(f" [*] RabbitMQ: {os.getenv('RABBITMQ_URL', 'amqp://localhost:5672/')}")
    print(f" [*] Almacenamiento: {os.getenv('STORAGE_PATH', 'data/notifications.json')}")
    
    # Crear directorio de datos si no existe
    storage_path = os.getenv('STORAGE_PATH', 'data/notifications.json')
    storage_dir = os.path.dirname(storage_path)
    if storage_dir:
        os.makedirs(storage_dir, exist_ok=True)
    
    # Iniciar consumidor de RabbitMQ en segundo plano
    thread = threading.Thread(target=start_rabbitmq_consumer, daemon=True)
    thread.start()
    print(" [✓] Sistema de mensajería RabbitMQ iniciado en segundo plano.")

@app.on_event("shutdown")
def shutdown_event():
    """Evento que se ejecuta al cerrar la aplicación"""
    print(" [*] Cerrando Notification Service...")