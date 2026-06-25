# ===================================================================
# ✅ TRAINING ENTRY POINT
# Run this file to train the DistilBERT classifier:
#   python train.py
# ===================================================================

from core.config import device, TRAIN_MODEL_NAME
from training.downloader import ensure_dataset
from training.dataset    import load_data
from training.trainer    import (
    build_model,
    build_optimizer_scheduler,
    train_one_epoch,
    validate,
    save_model,
)
from transformers import DistilBertTokenizer
from core.config import TRAIN_EPOCHS

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":

    print(f"✅ Using device: {device}")

    # Step 1 — ensure dataset exists (auto-download if needed)
    ensure_dataset()

    # Step 2 — load data → DataLoaders
    train_loader, val_loader = load_data()

    # Step 3 — build model
    model = build_model()

    # Step 4 — optimizer + scheduler
    optimizer, scheduler = build_optimizer_scheduler(model, train_loader)

    # Step 5 — load tokenizer (needed for saving later)
    tokenizer = DistilBertTokenizer.from_pretrained(TRAIN_MODEL_NAME)

    # Step 6 — training loop
    for epoch in range(1, TRAIN_EPOCHS + 1):
        print(f"\n🏋️  Training Epoch {epoch}/{TRAIN_EPOCHS}...")

        avg_loss = train_one_epoch(
            model, train_loader, optimizer, scheduler, epoch
        )
        print(f"📉 Epoch {epoch} Train Loss: {avg_loss:.4f}")

        print(f"🔍 Validating Epoch {epoch}...")
        validate(model, val_loader, epoch)

    # Step 7 — save model + tokenizer
    save_model(model, tokenizer)
