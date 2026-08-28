from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings
from services.ai_models import ml_models
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_models.load_models(settings.YOLO_MODEL_PATH)
    yield
    ml_models.yolo_model = None
    ml_models.ocr_engine = None

app = FastAPI(
    title="Deteksi Plat Nomor API",
    description="API untuk mendeteksi plat nomor kendaraan menggunakan YOLOv11 & PaddleOCR",
    lifespan=lifespan
)

app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {"Status": "Server Aktif dan Model Siap Digunakan!"}