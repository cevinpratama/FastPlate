from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from PIL import Image
import io
from ultralytics import YOLO

app = FastAPI()
model = YOLO(r"D:\Coding\Web\Back-End\plat_fast\yolov11s_fold3.pt")

def ocr(image):
    return "BL123H"

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

