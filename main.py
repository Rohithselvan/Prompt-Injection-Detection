# ===================================================================
# ✅ FASTAPI ENTRY POINT
# Start the server:
#   uvicorn main:app --reload --host 0.0.0.0 --port 8000
# ===================================================================

import time
import uuid
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.config     import BASE_DIR, device
from core.preprocess import clean_text
from core.ocr        import extract_text_from_image
from core.asr        import transcribe_audio
from pipeline.heuristic   import HeuristicFilter
from pipeline.classifier  import predict, get_label
from pipeline.gemini      import generate_response

# ---------------------------------------------------------
# APP INIT
# ---------------------------------------------------------
app = FastAPI(
    title       = "Prompt Injection Detector API",
    description = "2-layer security pipeline: Heuristic + DistilBERT + Gemini",
    version     = "1.0.0",
)

# Static files & frontend
app.mount(
    "/static",
    StaticFiles(directory=f"{BASE_DIR}/static"),
    name="static",
)

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(f"{BASE_DIR}/static/index.html")

# ---------------------------------------------------------
# STARTUP BANNER
# ---------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    print(f"""
╔══════════════════════════════════════════╗
║   🛡️  Prompt Injection Detector API      ║
║   Device  : {str(device).upper():<30}║
║   Model   : DistilBERT (local)           ║
║   Docs    : http://localhost:8000/docs   ║
╚══════════════════════════════════════════╝
""")

# ---------------------------------------------------------
# FILTER INSTANCE
# ---------------------------------------------------------
_heuristic = HeuristicFilter()

# ---------------------------------------------------------
# INGEST ENDPOINT
# ---------------------------------------------------------
@app.post("/ingest")
async def ingest(
    text:     Optional[str]        = Form(None),
    image:    Optional[UploadFile] = File(None),
    audio:    Optional[UploadFile] = File(None),
    metadata: Optional[str]        = Form(None),
):
    start_total    = time.time()
    request_id     = str(uuid.uuid4())
    extracted_text = text
    ocr_time       = 0.0
    asr_time       = 0.0

    # ── Image OCR ────────────────────────────────────────────
    if image:
        t0             = time.time()
        extracted_text = await extract_text_from_image(image)
        ocr_time       = round(time.time() - t0, 4)

    # ── Audio transcription ───────────────────────────────────
    if audio:
        t0             = time.time()
        extracted_text = await transcribe_audio(audio)
        asr_time       = round(time.time() - t0, 4)

    # ── Text cleaning ─────────────────────────────────────────
    cleaned_text = clean_text(extracted_text or "")

    # ── Layer 1: Heuristic scan ───────────────────────────────
    t0               = time.time()
    heuristic_result = _heuristic.scan(cleaned_text)
    heuristic_time   = round(time.time() - t0, 4)

    # ── Layer 2: DistilBERT + Layer 3: Gemini ─────────────────
    safe_to_send    = heuristic_result["passed"]
    model_result    = None
    gemini_response = None
    model_time      = 0.0
    gemini_time     = 0.0

    if safe_to_send:
        t0                   = time.time()
        label_id, confidence = predict(cleaned_text)
        model_time           = round(time.time() - t0, 4)
        label_name           = get_label(label_id)

        model_result = {
            "prediction": label_name,
            "confidence": confidence,
            "time_sec":   model_time,
        }

        if label_name == "Safe":
            t0              = time.time()
            gemini_response = generate_response(cleaned_text)
            gemini_time     = round(time.time() - t0, 4)
        else:
            safe_to_send    = False
            gemini_response = {
                "error": "DistilBERT flagged as unsafe — not sent to Gemini."
            }
    else:
        gemini_response = {
            "error": "Heuristic scan flagged as unsafe — not sent to Gemini."
        }

    # ── Response ──────────────────────────────────────────────
    return {
        "request_id":      request_id,
        "metadata":        metadata,
        "final_text":      cleaned_text,
        "heuristic":       {**heuristic_result, "time_sec": heuristic_time},
        "model":           model_result,
        "ocr_time_sec":    ocr_time,
        "asr_time_sec":    asr_time,
        "gemini_time_sec": gemini_time,
        "total_time_sec":  round(time.time() - start_total, 4),
        "safe_to_send":    safe_to_send,
        "gemini_response": gemini_response,
        "image_name":      image.filename if image else None,
        "audio_name":      audio.filename if audio else None,
    }
