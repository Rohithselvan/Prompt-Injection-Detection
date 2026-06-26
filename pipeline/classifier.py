# ===================================================================
# ✅ LAYER 2 — DISTILBERT CLASSIFIER
# Loads the fine-tuned model and runs binary inference
# ===================================================================

import torch
import torch.nn.functional as F

from core.config import DISTILBERT_MAX_LEN, LABEL_NAMES, device
from core.model_loader import load_model   # ✅ NEW IMPORT

# ---------------------------------------------------------
# LOAD MODEL + TOKENIZER (once at import time)
# ---------------------------------------------------------
print("⏳ Loading DistilBERT model...")

try:
    # ✅ Use unified loader (local OR Hugging Face)
    _model, _tokenizer = load_model()

    print("✅ DistilBERT loaded successfully.")

except Exception as e:
    print(f"""
❌ Failed to load DistilBERT model!

   It tried:
   1. Local /model folder
   2. Hugging Face fallback

   Error: {e}
""")
    raise SystemExit(1)

# ---------------------------------------------------------
# INFERENCE
# ---------------------------------------------------------
def predict(text: str) -> tuple[int, float]:
    """
    Run DistilBERT inference on the given text.

    Returns:
        label      : int   — 0 (Safe) or 1 (Unsafe)
        confidence : float — confidence percentage (0–100)
    """
    inputs = _tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=DISTILBERT_MAX_LEN,
    ).to(device)

    with torch.no_grad():
        outputs = _model(**inputs)

    probs = F.softmax(outputs.logits, dim=1)
    confidence, pred = torch.max(probs, dim=1)

    return pred.item(), round(confidence.item() * 100, 2)


def get_label(label_id: int) -> str:
    """Convert numeric label to human-readable string."""
    return LABEL_NAMES.get(label_id, "Unknown")
