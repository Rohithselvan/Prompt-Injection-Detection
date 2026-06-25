# ===================================================================
# ✅ ASR MODULE
# OpenAI Whisper-based audio transcription
# ===================================================================

import os
import tempfile
import whisper  # type: ignore

# ---------------------------------------------------------
# LOAD WHISPER ONCE AT IMPORT TIME
# ---------------------------------------------------------
print("⏳ Loading Whisper model...")
_whisper_model = whisper.load_model("base")
print("✅ Whisper loaded.")

async def transcribe_audio(audio_file) -> str:
    """
    Accept a FastAPI UploadFile, save it to a temp file,
    transcribe with Whisper, and return the transcript text.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio_file.read())
        tmp_path = tmp.name

    try:
        result = _whisper_model.transcribe(tmp_path)
    finally:
        os.remove(tmp_path)

    return result["text"].strip()