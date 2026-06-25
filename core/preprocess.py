# ===================================================================
# ✅ TEXT PREPROCESSING
# Emoji removal and text cleaning utilities
# ===================================================================

import re

# ---------------------------------------------------------
# EMOJI PATTERN
# ---------------------------------------------------------
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002500-\U00002BEF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"
    "\u3030"
    "]+"
)

def remove_emojis(text: str) -> str:
    """Strip all emoji characters from a string."""
    return EMOJI_PATTERN.sub(r"", text or "")

def clean_text(text: str) -> str:
    """
    Full text cleaning pipeline:
    1. Remove emojis
    2. Collapse excessive whitespace
    3. Strip leading/trailing whitespace
    """
    text = remove_emojis(text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()