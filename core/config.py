# ===================================================================
# ✅ CORE CONFIG
# ===================================================================

import os
import torch
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(BASE_DIR, "model")  # model folder

# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
genai.configure(api_key=GOOGLE_API_KEY)

# ---------------------------------------------------------
# DEVICE
# ---------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------------------------------------------------
# TESSERACT — Windows path auto-detection
# ---------------------------------------------------------
_TESS_WIN = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------------------------------------------------
# DISTILBERT
# ---------------------------------------------------------
DISTILBERT_MAX_LEN = 256

LABEL_NAMES = {0: "Safe", 1: "Unsafe"}

# ---------------------------------------------------------
# TRAINING HYPERPARAMETERS
# ---------------------------------------------------------
TRAIN_MODEL_NAME  = "distilbert-base-uncased"
TRAIN_DATA_PATH   = os.path.join(BASE_DIR, "data.csv")
TRAIN_MAX_LEN     = 256
TRAIN_BATCH_SIZE  = 16
TRAIN_EPOCHS      = 2
TRAIN_LR          = 2e-5
TRAIN_RANDOM_SEED = 42
TRAIN_SAVE_PATH   = BASE_DIR

# ---------------------------------------------------------
# HUGGING FACE DATASET
# ---------------------------------------------------------
HF_REPO_ID  = "Rohith1872/prompt-injection-dataset"
HF_FILENAME = "data.csv"

# ---------------------------------------------------------
# ✅ HUGGING FACE MODEL (IMPORTANT)
# ---------------------------------------------------------
HF_MODEL_ID = "Rohith1872/DistilBERT_Classifier"

# Minimum required files to consider model "present"
LOCAL_MODEL_FILES = [
    "config.json",
    "model.safetensors",
    "tokenizer_config.json",
    "vocab.txt"
]
