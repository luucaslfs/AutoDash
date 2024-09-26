import logging
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .services.state_manager import cleanup_expired_entries
from .api.v1 import router as api_v1_router
from dotenv import load_dotenv
from .core.config import settings

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Define o nível mínimo de logging
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Envia logs para o console
    ]
)

logger = logging.getLogger(__name__)
logger.info("Iniciando a aplicação AutoDash API")

app = FastAPI(title=settings.APP_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://autodash-front.onrender.com"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Starts cleanup thread
cleanup_thread = threading.Thread(target=cleanup_expired_entries, daemon=True)
cleanup_thread.start()

# Include the v1 API router
app.include_router(api_v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)