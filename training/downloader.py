    # ===================================================================
# ✅ DATASET DOWNLOADER
# Auto-downloads the dataset from Hugging Face if not found locally
# ===================================================================

import os
from huggingface_hub import hf_hub_download  # type: ignore

from core.config import HF_REPO_ID, HF_FILENAME, TRAIN_DATA_PATH

def ensure_dataset() -> None:
    """
    Check if data.csv exists locally.
    If not, download it automatically from Hugging Face.
    Exits the process if the download fails.
    """
    if os.path.exists(TRAIN_DATA_PATH):
        print("✅ Dataset found locally — skipping download.")
        return

    print(f"⚠️  Dataset not found at: {TRAIN_DATA_PATH}")
    print(f"⏳ Downloading from Hugging Face ({HF_REPO_ID})...")

    try:
        hf_hub_download(
            repo_id   = HF_REPO_ID,
            filename  = HF_FILENAME,
            repo_type = "dataset",
            local_dir = os.path.dirname(TRAIN_DATA_PATH),
        )
        print("✅ Dataset downloaded successfully!")

    except Exception as e:
        print(f"❌ Failed to download dataset: {e}")
        print(f"   Please manually place data.csv in: {os.path.dirname(TRAIN_DATA_PATH)}")
        print(f"   Dataset URL: https://huggingface.co/datasets/{HF_REPO_ID}")
        raise SystemExit(1)