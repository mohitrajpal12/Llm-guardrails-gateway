import yaml
from functools import lru_cache
from pathlib import Path

POLICY_PATH = Path(__file__).parent.parent / "config" / "policy.yaml"


@lru_cache(maxsize=1)
def load_policy() -> dict:
    with open(POLICY_PATH, "r") as f:
        return yaml.safe_load(f)


def get_input_policy() -> dict:
    return load_policy().get("input", {})


def get_output_policy() -> dict:
    return load_policy().get("output", {})


def get_retry_policy() -> dict:
    return load_policy().get("retry", {})
