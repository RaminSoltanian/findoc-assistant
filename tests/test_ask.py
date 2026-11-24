from fastapi.testclient import TestClient
from app import main
from app.schemas import Answer

client = TestClient(main.app)

FAKE = Answer(answer="25 years", confidence="high",
              topic="mortgage", needs_source_document=True)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ask_returns_fixed_format(monkeypatch):
    monkeypatch.setattr(main, "ask_llm", lambda q: (FAKE, {}))
    r = client.post("/ask", json={"question": "Max amortization?"})
    assert r.status_code == 200
    assert r.json()["topic"] == "mortgage"
    assert set(r.json()) == {"answer", "confidence", "topic", "needs_source_document"}

def test_rejects_empty_question():
    r = client.post("/ask", json={"question": ""})
    assert r.status_code == 422

def test_rejects_too_long_question():
    r = client.post("/ask", json={"question": "x" * 1001})
    assert r.status_code == 422

def test_ai_failure_returns_502(monkeypatch):
    def broken(q):
        raise RuntimeError("AI service down")
    monkeypatch.setattr(main, "ask_llm", broken)
    r = client.post("/ask", json={"question": "Max amortization?"})
    assert r.status_code == 502