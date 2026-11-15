import re
import math
from typing import Tuple, List

class PromptSanitizer:
    """
    Sub-millisecond static analyzer intercepting prompt injections, jailbreaks,
    and hidden zero-width unicode characters before intent parsing.
    """

    INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+(instructions|prompts)", re.IGNORECASE),
        re.compile(r"system\s*:\s*you\s+are\s+now", re.IGNORECASE),
        re.compile(r"you\s+are\s+DAN", re.IGNORECASE),
        re.compile(r"act\s+as\s+(an?\s+unrestricted|root|admin)", re.IGNORECASE),
        re.compile(r"bypass\s+(all\s+)?(security|guardrails|safety)", re.IGNORECASE),
        re.compile(r"<\|im_start\|>", re.IGNORECASE),
        re.compile(r"<\|system\|>", re.IGNORECASE),
        re.compile(r"\[INST\]\s*<<SYS>>", re.IGNORECASE)
    ]

    ZERO_WIDTH_CHARS = [
        "\u200b", "\u200c", "\u200d", "\ufeff", "\u2060"
    ]

    @classmethod
    def sanitize(cls, text: str) -> Tuple[bool, str, List[str]]:
        """
        Returns (is_clean, sanitized_text, detected_threats)
        """
        threats = []
        if not text:
            return True, "", []

        # 1. Clean zero-width obfuscation characters
        sanitized = text
        for zw in cls.ZERO_WIDTH_CHARS:
            if zw in sanitized:
                threats.append("zero_width_obfuscation")
                sanitized = sanitized.replace(zw, "")

        # 2. Check known injection payloads
        for pattern in cls.INJECTION_PATTERNS:
            if pattern.search(sanitized):
                threats.append(f"prompt_injection_pattern:{pattern.pattern}")

        # 3. Shannon Entropy Check for Base64 / Hex hidden payloads
        words = sanitized.split()
        for w in words:
            if len(w) > 40:
                entropy = cls._shannon_entropy(w)
                if entropy > 4.5:
                    threats.append(f"high_entropy_obfuscated_token:{w[:10]}...")

        is_clean = len(threats) == 0
        return is_clean, sanitized.strip(), threats

    @staticmethod
    def _shannon_entropy(data: str) -> float:
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        frequencies = {}
        for c in data:
            frequencies[c] = frequencies.get(c, 0) + 1
        for count in frequencies.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy
