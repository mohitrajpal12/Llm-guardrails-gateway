
from llm.gemini_client import call_llm
def test_gemini():
    response = call_llm("Say hello in one sentence.")
    print(response)
    assert len(response) > 0

if __name__ == "__main__":
    test_gemini()
