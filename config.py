import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    YOLO_MODEL_PATH: str = os.getenv(
        "YOLO_MODEL_PATH", 
        r"D:\Coding\Web\Back-End\plat_fast\yolov11s_fold3.pt"
    )

settings = Settings()