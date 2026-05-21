from guardrails.input_guard import validate_input
from guardrails.output_guard import validate_output
from guardrails.policy_engine import get_retry_policy
from llm.gemini_client import call_llm


def run_with_guardrails(prompt: str) -> dict:
    policy = get_retry_policy()
    max_retries = policy.get("max_retries", 2)
    fallback = policy.get("fallback_message", "I'm sorry, I cannot process this request.")

    input_check = validate_input(prompt)
    if not input_check["valid"]:
        return {"success": False, "response": fallback, "reason": input_check["reason"]}

    current_prompt = prompt
    for attempt in range(max_retries + 2):
        response = call_llm(current_prompt)

        output_check = validate_output(response)
        if output_check["valid"]:
            return {"success": True, "response": response, "reason": None}

        if attempt < max_retries:
            current_prompt = (
                f"Your previous response was rejected because: {output_check['reason']}.\n"
                f"Please answer the following without violating that rule.\n\n"
                f"Original request: {prompt}"
            )

    return {"success": False, "response": fallback, "reason": output_check["reason"]}
