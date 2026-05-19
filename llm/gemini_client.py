import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))


def call_llm(prompt: str, system_instruction: str = None) -> str:
    if system_instruction:
        model = genai.GenerativeModel(
            os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            system_instruction=system_instruction
        )
    else:
        model = _model

    response = model.generate_content(prompt)
    return response.text.strip()
