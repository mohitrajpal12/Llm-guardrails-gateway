from guardrails.policy_engine import get_output_policy
from llm.gemini_client import call_llm


def _check_toxicity(text: str, threshold: float) -> bool:
    prompt = (
        f"Rate the toxicity of the following text on a scale from 0.0 to 1.0. "
        f"Only respond with a single float number, nothing else.\n\nText: {text}"
    )
    try:
        score = float(call_llm(prompt))
        return score >= threshold
    except ValueError:
        return False


def _check_blocked_topics(text: str, blocked_topics: list[str]) -> list[str]:
    topics_str = ", ".join(blocked_topics)
    prompt = (
        f"Does the following text discuss any of these topics: {topics_str}?\n"
        f"Reply with only the matching topics as a comma-separated list, or 'none' if none match.\n\n"
        f"Text: {text}"
    )
    result = call_llm(prompt).strip().lower()
    if result == "none":
        return []
    return [t.strip() for t in result.split(",") if t.strip()]


def validate_output(response: str) -> dict:
    policy = get_output_policy()

    if len(response) > policy.get("max_response_length", 1000):
        return {"valid": False, "reason": f"Response exceeds maximum length of {policy['max_response_length']} characters."}

    if _check_toxicity(response, policy.get("toxicity_threshold", 0.7)):
        return {"valid": False, "reason": "Toxic content detected in response."}

    blocked = _check_blocked_topics(response, policy.get("block_topics", []))
    if blocked:
        return {"valid": False, "reason": f"Blocked topic in response: {', '.join(blocked)}"}

    return {"valid": True, "reason": None}
