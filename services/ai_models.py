from ultralytics import YOLO
from paddleocr import PaddleOCR

class AIModels:
    def __init__(self):
        self.yolo_model = None
        self.ocr_engine = None

    def load_models(self, yolo_path: str):
        print("Mulai memuat model YOLO...")
        self.yolo_model = YOLO(yolo_path)
        
        print("Mulai memuat model PaddleOCR...")
        self.ocr_engine = PaddleOCR(use_angle_cls=True, lang='en', enable_mkldnn=False)
        print("Semua model berhasil dimuat!")

ml_models = AIModels()