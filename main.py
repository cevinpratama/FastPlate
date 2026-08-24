from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from PIL import Image
import io
from ultralytics import YOLO
from paddleocr import PaddleOCR
import numpy as np 
import cv2

app = FastAPI()
model = YOLO(r"D:\Coding\Web\Back-End\plat_fast\yolov11s_fold3.pt")
ocr_engine = PaddleOCR(use_angle_cls=True, lang='en', enable_mkldnn=False)

def preprocess_image(image_pil):

    
    img_np = np.array(image_pil.convert("RGB"))
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    scale = 4
    img_upscaled = cv2.resize(
        img_bgr,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    # Tambahkan padding
    img_padded = cv2.copyMakeBorder(
        img_upscaled,
        top=20,
        bottom=20,
        left=20,
        right=20,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )

    cv2.imwrite("debug_paddle.jpg", img_padded)

    return img_padded

def ocr(image_pil):
    try:
        img_siap_ocr = preprocess_image(image_pil)

        result = ocr_engine.ocr(img_siap_ocr)

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
            
        else:
             return f"Struktur data OCR tidak dikenali: Tipe {type(data_ocr)}"

        if len(teks_gabungan) < 4:
            return "Terbaca namun keliru: " + teks_gabungan
        
        return teks_gabungan
        
    except Exception as e:
        import traceback
        print("--- ERROR PADDLEOCR ---")
        traceback.print_exc() 
        return f"Error OCR: {e}"

@app.post("/plat")
async def deteksi_plat(file: UploadFile = File(...)):

    try:

        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        result = model(image)
        hasil_deteksi = []

        for box in result[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cropped_image = image.crop((x1, y1, x2, y2))

            text_plate = ocr(cropped_image)
            hasil_deteksi.append({
                "teks_plate": text_plate,
                "confidence_yolo": round(conf,2),
                "koordinat": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            })
            jumlah_deteksi = len(hasil_deteksi)

        return {
                "Pesan": f"Terdeteksi plat dengan jumlah {jumlah_deteksi}",
                "Jumlah": jumlah_deteksi,
                "Hasil OCR": hasil_deteksi
            }
    except Exception as e:
        return {"error": str(e)}

