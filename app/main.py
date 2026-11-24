import logging
from fastapi import FastAPI, HTTPException
from app.schemas import AskRequest, Answer
from app.llm import ask_llm

log = logging.getLogger("findoc")
app = FastAPI(title="FinDoc Assistant")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=Answer)
def ask(req: AskRequest):
    try:
        answer, usage = ask_llm(req.question)
    except Exception as e:
        log.exception("LLM call failed")
        raise HTTPException(status_code=502, detail="The AI service failed. Try again.")
    log.info("tokens used: %s", usage)
    return answer