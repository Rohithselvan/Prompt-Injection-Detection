# ===================================================================
# ✅ OCR MODULE
# Tesseract-based image text extraction
# ===================================================================

import os
import tempfile
from PIL import Image
import pytesseract  # type: ignore

from core.config import _TESS_WIN

# ---------------------------------------------------------
# WINDOWS PATH AUTO-DETECTION
# ---------------------------------------------------------
if os.path.exists(_TESS_WIN):
    pytesseract.pytesseract.tesseract_cmd = _TESS_WIN

async def extract_text_from_image(image_file) -> str:
    """
    Accept a FastAPI UploadFile, save it to a temp file,
    run Tesseract OCR, and return the extracted text.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(await image_file.read())
        tmp_path = tmp.name

    try:
        extracted = pytesseract.image_to_string(Image.open(tmp_path))
    finally:
        os.remove(tmp_path)

    return extracted.strip()