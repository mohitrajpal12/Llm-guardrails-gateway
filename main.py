from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.retry import run_with_guardrails

app = FastAPI(title="LLM Guardrails Gateway", version="1.0.0")


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    success: bool
    response: str
    reason: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=PromptResponse)
def chat(request: PromptRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    result = run_with_guardrails(request.prompt)
    return PromptResponse(**result)
