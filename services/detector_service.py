from PIL import Image, ImageOps
from services.image_processor import preprocess_image_for_ocr
from services.ai_models import ml_models
import traceback
import numpy as np
import re


def parse_ktp_ocr(ocr_items: list) -> dict:
    result = {}
    
    KNOWN_FIELDS = [
        "NIK", "Nama", "Tempat/Tgl Lahir", "Jenis Kelamin", 
        "Gol. Darah", "Alamat", "RT/RW", "Kel/Desa", 
        "Kecamatan", "Agama", "Status Perkawinan", 
        "Pekerjaan", "Kewarganegaraan", "Berlaku Hingga"
    ]
    
    pattern_fields = "|".join([re.escape(f) for f in KNOWN_FIELDS])
    inline_regex = re.compile(rf"^({pattern_fields})\s*:\s*(.*)$", re.IGNORECASE)
    
    i = 0
    n = len(ocr_items)
    
    while i < n:
        raw_text = ocr_items[i]["text"].strip()
        
        match_inline = inline_regex.match(raw_text)
        if match_inline:
            key, val = match_inline.groups()
            result[key.title()] = val.strip()
            i += 1
            continue
            
        if i + 1 < n:
            next_text = ocr_items[i + 1]["text"].strip()
            if next_text.startswith(":"):
                result[raw_text] = next_text.lstrip(":").strip()
                i += 2
                continue
        
        if "PROVINSI" in raw_text.upper():
            result["Provinsi"] = raw_text.replace("PROVINSI", "").strip()
        elif any(k in raw_text.upper() for k in ["KOTA", "KABUPATEN", "JAKARTA"]):
            result["Kota/Kabupaten"] = raw_text.strip()
            
        i += 1
        
    return result


def olah_ocr_ktp(image_pil: Image.Image) -> dict:
    image_padded = ImageOps.expand(image_pil.convert("RGB"), border=40, fill="white")
    img_np = np.array(image_padded)
    
    try:
        raw_result = ml_models.ocr_engine.ocr(img_np)
        if not raw_result:
            return {}

        res = raw_result[0]

        texts = res.get("rec_texts", [])
        scores = res.get("rec_scores", [])
        polys = res.get("dt_polys", res.get("rec_polys", []))

        # 1. Kumpulkan raw OCR detection
        raw_items = [
            {
                "text": str(text),
                "confidence": round(float(score), 4),
            }
            for text, score, poly in zip(texts, scores, polys)
        ]

        # 2. Parsing list raw menjadi dictionary terstruktur
        hasil_terstruktur = parse_ktp_ocr(raw_items)

        return hasil_terstruktur

    except Exception as e:
        print(f"Error OCR: {e}")
        return {}


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