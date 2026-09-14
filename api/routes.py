import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
from services.detector_service import process_plate_detection, olah_ocr_ktp
from pydantic import BaseModel

router = APIRouter()

class Data(BaseModel):
    nput: int


@router.post("/plat")
def deteksi_plat_endpoint(file: UploadFile = File(...)):
    try:
        image_bytes = file.file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        hasil_deteksi = process_plate_detection(image)
        jumlah_deteksi = len(hasil_deteksi)

        return {
            "Pesan": f"Terdeteksi plat dengan jumlah {jumlah_deteksi}",
            "Jumlah": jumlah_deteksi,
            "Hasil OCR": hasil_deteksi
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ktp")
def ocr_ktp(file:UploadFile = File(...)):
    try:
        image_bytes = file.file.read()
        image = Image.open(io.BytesIO(image_bytes))
        ocr = olah_ocr_ktp(image)
        return{
            "Terdeteksi bro": ocr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/a")
def coba(nput : Data):
    nputt = nput.nput + 2
    return { "asuw" : nputt}