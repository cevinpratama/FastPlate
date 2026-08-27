from PIL import Image
from services.image_processor import preprocess_image_for_ocr
from services.ai_models import ml_models
import traceback

def run_ocr(image_pil: Image.Image) -> str:
    try:
        img_siap_ocr = preprocess_image_for_ocr(image_pil)
        
        # Panggil ocr_engine dari memori (ai_models.py)
        result = ml_models.ocr_engine.ocr(img_siap_ocr)

        if not result or len(result) == 0:
            return "Plat tidak terbaca (Result Kosong)"
        
        data_ocr = result[0]
        if not data_ocr:
            return "Plat tidak terbaca (Elemen pertama kosong)"

        teks_gabungan = ""

        if isinstance(data_ocr, dict) and 'rec_texts' in data_ocr:
            list_teks = data_ocr['rec_texts'] 
            teks_mentah = "".join(list_teks)
            teks_bersih = ''.join(char for char in teks_mentah if char.isalnum()).upper()
            teks_gabungan = teks_bersih
        # Tambahan fallback standar output PaddleOCR (berupa List)
        elif isinstance(data_ocr, list):
            list_teks = [line[1][0] for line in data_ocr]
            teks_mentah = "".join(list_teks)
            teks_bersih = ''.join(char for char in teks_mentah if char.isalnum()).upper()
            teks_gabungan = teks_bersih
        else:
             return f"Struktur data OCR tidak dikenali: Tipe {type(data_ocr)}"

        if len(teks_gabungan) < 4:
            return "Terbaca namun keliru: " + teks_gabungan
        
        return teks_gabungan
        
    except Exception as e:
        print("--- ERROR PADDLEOCR ---")
        traceback.print_exc() 
        return f"Error OCR: {e}"

def process_plate_detection(image: Image.Image) -> list:
    # Panggil YOLO dari memori
    result = ml_models.yolo_model(image)
    hasil_deteksi = []

    for box in result[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cropped_image = image.crop((x1, y1, x2, y2))

        text_plate = run_ocr(cropped_image)
        hasil_deteksi.append({
            "teks_plate": text_plate,
            "confidence_yolo": round(conf, 2),
            "koordinat": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
        })

    return hasil_deteksi