# ===================================================================
# ✅ LAYER 3 — GEMINI RESPONSE
# Sends safe, verified text to Google Gemini for a reply
# ===================================================================

import google.generativeai as genai  # type: ignore

# ---------------------------------------------------------
# GEMINI CALL
# ---------------------------------------------------------
def generate_response(text: str) -> dict:
    """
    Send text to Google Gemini 2.5 Flash and return the response.

    Returns:
        dict with either:
            {"gemini_reply": "...response text..."}
        or on error:
            {"error": "...error message..."}
    """
    try:
        model    = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(text)
        return {"gemini_reply": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}