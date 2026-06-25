# ===================================================================
# ✅ TRAINER MODULE
# Model setup, training loop, validation loop, and model saving
# ===================================================================

import os
import torch
from transformers import (
    DistilBertForSequenceClassification,
    get_linear_schedule_with_warmup,
)
from torch.optim import AdamW
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, classification_report
from tqdm import tqdm

from core.config import (
    TRAIN_MODEL_NAME,
    TRAIN_EPOCHS,
    TRAIN_LR,
    TRAIN_SAVE_PATH,
    device,
)

# ---------------------------------------------------------
# BUILD MODEL
# ---------------------------------------------------------
def build_model() -> DistilBertForSequenceClassification:
    """Load DistilBERT from HuggingFace Hub and move to device."""
    print("\n🤖 Loading DistilBERT model...")
    model = DistilBertForSequenceClassification.from_pretrained(
        TRAIN_MODEL_NAME,
        num_labels=2,
    ).to(device)
    return model

# ---------------------------------------------------------
# BUILD OPTIMIZER + SCHEDULER
# ---------------------------------------------------------
def build_optimizer_scheduler(
    model: DistilBertForSequenceClassification,
    train_loader: DataLoader,
) -> tuple:
    """
    Create AdamW optimizer and linear warmup scheduler.

    Returns:
        optimizer : AdamW
        scheduler : linear warmup scheduler
    """
    optimizer   = AdamW(model.parameters(), lr=TRAIN_LR)
    total_steps = len(train_loader) * TRAIN_EPOCHS

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps   = int(0.1 * total_steps),
        num_training_steps = total_steps,
    )
    return optimizer, scheduler

# ---------------------------------------------------------
# TRAINING LOOP
# ---------------------------------------------------------
def train_one_epoch(
    model:       DistilBertForSequenceClassification,
    train_loader: DataLoader,
    optimizer:   AdamW,
    scheduler,
    epoch:       int,
) -> float:
    """
    Run one full training epoch.

    Returns:
        avg_loss : float — average training loss for this epoch
    """
    model.train()
    total_loss = 0.0

    for batch in tqdm(train_loader, desc=f"Training Epoch {epoch}"):
        optimizer.zero_grad()

        input_ids      = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels         = batch["labels"].to(device)

        outputs = model(
            input_ids      = input_ids,
            attention_mask = attention_mask,
            labels         = labels,
        )

        loss = outputs.loss
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)

# ---------------------------------------------------------
# VALIDATION LOOP
# ---------------------------------------------------------
def validate(
    model:      DistilBertForSequenceClassification,
    val_loader: DataLoader,
    epoch:      int,
) -> float:
    """
    Run validation and print accuracy + classification report.

    Returns:
        accuracy : float — validation accuracy (0.0–1.0)
    """
    model.eval()
    preds, true_labels = [], []

    with torch.no_grad():
        for batch in tqdm(val_loader, desc="Validating"):
            input_ids      = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels         = batch["labels"].to(device)

            outputs = model(
                input_ids      = input_ids,
                attention_mask = attention_mask,
            )

            preds.extend(torch.argmax(outputs.logits, dim=1).cpu().numpy())
            true_labels.extend(labels.cpu().numpy())

    acc = accuracy_score(true_labels, preds)
    print(f"✅ Epoch {epoch} Validation Accuracy: {acc * 100:.2f}%")
    print(classification_report(true_labels, preds, target_names=["Safe", "Unsafe"]))

    return acc

# ---------------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------------
def save_model(model, tokenizer):
    save_dir = "model"

    os.makedirs(save_dir, exist_ok=True)

    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)

    print(f"\n✅ Model saved to: {save_dir}")