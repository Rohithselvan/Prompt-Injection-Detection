# ===================================================================
# ✅ LAYER 1 — HEURISTIC FILTER
# Fast pattern-matching pre-filter before the ML model
# ===================================================================

import re
from enum import Enum

class RiskLevel(Enum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"

class HeuristicFilter:
    """
    Layer 1 security filter.

    Scans input text for:
    - Quick-safe patterns  → skip heavy checks entirely
    - Whitelisted content  → structured/code content, always safe
    - Suspicious keywords  → phishing, social engineering signals
    - Injection markers    → prompt injection attack signatures
    - Obfuscation patterns → encoding tricks to bypass filters
    """

    def __init__(self):

        # ── Clearly benign phrasing ───────────────────────────
        self.quick_safe_patterns = [
            r"\b\d{1,2}:\d{2}\b",
            r"shopping list:.*",
            r"reminder:.*",
            r"note:.*",
            r"meeting at.*",
            r"time:.*; location:.*",
            r"chapter \d+",
            r"backup your project.*",
        ]

        # ── Whitelisted code / structured content ─────────────
        self.whitelist_patterns = [
            r"(x\s*=\s*\d+;\s*y\s*=\s*x\s*[+\-\/]\s*\d+)",
            r"def\s+\w+\(\):",
            r"SQL:\s*SELECT\s+.*;",
            r"YAML:\s*\w+:\s*.*",
        ]

        # ── Suspicious keyword patterns ───────────────────────
        self.suspicious_patterns = [
            r"send\s+money",
            r"transfer\s+\d+",
            r"wire\s+funds",
            r"bank\s+account",
            r"credit\s+card",
            r"otp",
            r"https?://\S+",
            r"bit\.ly/\S+",
            r"click\s+this\s+link",
            r"free\s+reward",
            r"urgent",
            r"immediately",
            r"before\s+midnight",
            r"else\s+your\s+account\s+will\s+be\s+locked",
            r"verify\s+your\s+account",
            r"one[-\s]?time\s+password",
            r"claim\s+your\s+prize",
            r"payment\s+required",
            r"wire\s+the\s+money",
            r"send\s+otp",
        ]

        # ── Injection & obfuscation patterns ──────────────────
        self.injection_patterns = {
            "injection_markers": [
                r"###?\s*[^#\n]+###?",
                r"---+\s*[^-\n]+---+",
                r"\[INST\]|\[/INST\]",
                r"<\|.*?\|>",
                r"```\s*(prompt|instruction|system)",
            ],
            "obfuscation": [
                r"[a-zA-Z0-9+/]{20,}={0,2}",
                r"\\u[0-9a-fA-F]{4}",
                r"&#x?[0-9a-fA-F]+;",
                r"%[0-9a-fA-F]{2}",
                r"[^\x00-\x7F]+.*[^\x00-\x7F]+",
            ],
        }

    # ----------------------------------------------------------
    def scan(self, text: str) -> dict:
        """
        Run the full heuristic scan on the given text.

        Returns a dict with:
            passed          : bool   — True if safe to proceed
            risk            : str    — "low" | "medium" | "high"
            score           : float  — cumulative threat score
            matched_patterns: dict   — patterns that triggered
            quick_safe      : bool   — True if quick-safe matched
        """
        if not text or not isinstance(text, str):
            return {
                "passed":           True,
                "risk":             RiskLevel.LOW.value,
                "score":            0.0,
                "matched_patterns": {},
                "quick_safe":       False,
            }

        text_lower       = text.lower()
        matched_patterns = {}
        total_score      = 0.0
        quick_safe       = False

        # Quick-safe check
        for pattern in self.quick_safe_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE | re.MULTILINE):
                quick_safe = True
                break

        # Whitelist check
        for pattern in self.whitelist_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE | re.MULTILINE):
                quick_safe = True

        # Suspicious keyword scoring
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE | re.MULTILINE):
                matched_patterns.setdefault("suspicious", []).append(pattern)
                total_score += 1.0

        # Injection & obfuscation scoring
        for category, patterns in self.injection_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE | re.MULTILINE):
                    matched_patterns.setdefault(category, []).append(pattern)
                    total_score += 1.0

        # Risk classification
        if total_score >= 2.0:
            risk = RiskLevel.HIGH
        elif total_score >= 1.0:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        return {
            "passed":           risk == RiskLevel.LOW,
            "risk":             risk.value,
            "score":            round(total_score, 2),
            "matched_patterns": matched_patterns,
            "quick_safe":       quick_safe,
        }