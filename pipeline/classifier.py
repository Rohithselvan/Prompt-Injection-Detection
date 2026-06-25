# ===================================================================
# ✅ LAYER 2 — DISTILBERT CLASSIFIER
# Loads the fine-tuned model and runs binary inference
# ===================================================================

import torch
import torch.nn.functional as F
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

from core.config import MODEL_PATH, DISTILBERT_MAX_LEN, LABEL_NAMES, device

# ---------------------------------------------------------
# LOAD MODEL + TOKENIZER (once at import time)
# ---------------------------------------------------------
print(f"⏳ Loading DistilBERT from: {MODEL_PATH}")

try:
    _tokenizer = DistilBertTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
    )
    _model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
    ).to(device)
    _model.eval()
    print("✅ DistilBERT loaded successfully.")

except Exception as e:
    print(f"""
❌ Failed to load DistilBERT model!
   Expected model files in : {MODEL_PATH}
   Have you run train.py yet?

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
        return_tensors = "pt",
        truncation     = True,
        padding        = True,
        max_length     = DISTILBERT_MAX_LEN,
    ).to(device)

    with torch.no_grad():
        outputs = _model(**inputs)

    probs            = F.softmax(outputs.logits, dim=1)
    confidence, pred = torch.max(probs, dim=1)

    return pred.item(), round(confidence.item() * 100, 2)

def get_label(label_id: int) -> str:
    """Convert numeric label to human-readable string."""
    return LABEL_NAMES.get(label_id, "Unknown")