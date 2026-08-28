import cv2
import numpy as np
from PIL import Image

def preprocess_image_for_ocr(image_pil: Image.Image) -> np.ndarray:
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

    img_padded = cv2.copyMakeBorder(
        img_upscaled,
        top=20,
        bottom=20,
        left=20,
        right=20,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )

    return img_padded