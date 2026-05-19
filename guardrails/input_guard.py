import re
from presidio_analyzer import AnalyzerEngine
from guardrails.policy_engine import get_input_policy

_analyzer = AnalyzerEngine()

INJECTION_PATTERNS = [
    r"ignore\s+(previous|above|all)\s+instructions",
    r"you\s+are\s+now\s+(a|an)",
    r"act\s+as\s+(a|an)",
    r"pretend\s+(you\s+are|to\s+be)",
    r"jailbreak",
    r"dan\s+mode",
    r"developer\s+mode",
    r"bypass\s+(your\s+)?(rules|restrictions|guidelines|filters)",
    r"forget\s+(your\s+)?(instructions|training|rules)",
    r"you\s+have\s+no\s+restrictions",
]

_injection_regex = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)


def _check_pii(text: str, blocked_entities: list[str]) -> list[str]:
    results = _analyzer.analyze(text=text, entities=blocked_entities, language="en")
    return [r.entity_type for r in results]


def _check_injection(text: str) -> bool:
    return bool(_injection_regex.search(text))


def _check_blocked_topics(text: str, blocked_topics: list[str]) -> list[str]:
    text_lower = text.lower()
    return [topic for topic in blocked_topics if topic.lower() in text_lower]


def validate_input(prompt: str) -> dict:
    policy = get_input_policy()
    
    if len(prompt) > policy.get("max_prompt_length", 2000):
        return {"valid": False, "reason": f"Prompt exceeds maximum length of {policy['max_prompt_length']} characters."}

    pii_found = _check_pii(prompt, policy.get("block_pii", []))
    if pii_found:
        return {"valid": False, "reason": f"PII detected in prompt: {', '.join(pii_found)}"}

    if _check_injection(prompt):
        return {"valid": False, "reason": "Prompt injection attempt detected."}

    blocked = _check_blocked_topics(prompt, policy.get("block_topics", []))
    if blocked:
        return {"valid": False, "reason": f"Blocked topic detected: {', '.join(blocked)}"}

    return {"valid": True, "reason": None}


