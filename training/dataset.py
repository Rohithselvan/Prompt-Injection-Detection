# ===================================================================
# ✅ DATASET MODULE
# PromptDataset class + CSV loading + train/val split
# ===================================================================

import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer
from sklearn.model_selection import train_test_split
import torch

from core.config import (
    TRAIN_DATA_PATH,
    TRAIN_MAX_LEN,
    TRAIN_BATCH_SIZE,
    TRAIN_RANDOM_SEED,
    TRAIN_MODEL_NAME,
)

# ---------------------------------------------------------
# DATASET CLASS
# ---------------------------------------------------------
class PromptDataset(Dataset):
    """
    PyTorch Dataset for binary prompt classification.

    Args:
        texts     : list of raw text strings
        labels    : list of int labels (0 = Safe, 1 = Unsafe)
        tokenizer : HuggingFace tokenizer instance
        max_len   : maximum token length for padding/truncation
    """

    def __init__(self, texts: list, labels: list,
                 tokenizer: DistilBertTokenizer, max_len: int):
        self.texts     = texts
        self.labels    = labels
        self.tokenizer = tokenizer
        self.max_len   = max_len

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict:
        encoding = self.tokenizer(
            self.texts[idx],
            max_length     = self.max_len,
            padding        = "max_length",
            truncation     = True,
            return_tensors = "pt",
        )
        return {
            "input_ids":      encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels":         torch.tensor(self.labels[idx], dtype=torch.long),
        }

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
def load_data() -> tuple[DataLoader, DataLoader]:
    """
    Load data.csv, validate columns, split into train/val,
    tokenize, and return DataLoaders.
    """
    print("\n📂 Loading dataset...")
    df = pd.read_csv(TRAIN_DATA_PATH)

    # Rename prompt → text
    df = df.rename(columns={"prompt": "text"})

    assert "text" in df.columns and "label" in df.columns, \
        "❌ CSV must have 'text' and 'label' columns"

    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    print(f"✅ Total samples : {len(df)}")
    print(f"   Safe   (0)   : {(df['label'] == 0).sum()}")
    print(f"   Unsafe (1)   : {(df['label'] == 1).sum()}")

    # Train / validation split
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df["text"].tolist(),
        df["label"].tolist(),
        test_size=0.2,
        random_state=TRAIN_RANDOM_SEED,
        stratify=df["label"].tolist(),
    )

    print(f"✅ Train : {len(train_texts)} | Val : {len(val_texts)}")

    # Tokenizer
    tokenizer = DistilBertTokenizer.from_pretrained(TRAIN_MODEL_NAME)

    # Datasets
    train_dataset = PromptDataset(
        train_texts,
        train_labels,
        tokenizer,
        TRAIN_MAX_LEN
    )

    val_dataset = PromptDataset(
        val_texts,
        val_labels,
        tokenizer,
        TRAIN_MAX_LEN
    )

    # DataLoaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=TRAIN_BATCH_SIZE,
        shuffle=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=TRAIN_BATCH_SIZE,
        shuffle=False
    )

    return train_loader, val_loader