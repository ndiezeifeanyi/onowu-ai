PROMPT_INJECTION_MARKERS = {
    "ignore previous instructions",
    "ignore all previous",
    "developer message",
    "system prompt",
    "reveal your prompt",
    "disable safety",
    "jailbreak",
    "exfiltrate",
}


def detect_prompt_injection(text: str) -> list[str]:
    lowered = text.lower()
    return [marker for marker in PROMPT_INJECTION_MARKERS if marker in lowered]

