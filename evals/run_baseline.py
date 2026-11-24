"""Run the golden set against the running API and save a baseline."""
import csv, json
from pathlib import Path
import httpx

API = "http://localhost:8000/ask"
GOLDEN = Path("evals/golden_set.jsonl")
OUT = Path("evals/results/baseline_m1.csv")

def main():
    cases = [json.loads(line) for line in GOLDEN.read_text(encoding="utf-8").splitlines() if line.strip()]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows, passed = [], 0

    with httpx.Client(timeout=60) as client:
        for c in cases:
            r = client.post(API, json={"question": c["question"]})
            ans = r.json() if r.status_code == 200 else {"answer": f"HTTP {r.status_code}", "topic": ""}

            topic_ok = ans.get("topic") == c["expected_topic"]
            text = ans.get("answer", "").lower()
            keywords_ok = all(k.lower() in text for k in c["must_include"])
            passed += topic_ok and keywords_ok

            print(f"{c['id']}  topic {'OK ' if topic_ok else 'BAD'}  keywords {'OK ' if keywords_ok else 'BAD'}  {c['question'][:60]}")
            rows.append({
                "id": c["id"], "type": c["type"], "question": c["question"],
                "expected_answer": c["expected_answer"],
                "actual_answer": ans.get("answer", ""),
                "actual_topic": ans.get("topic", ""),
                "confidence": ans.get("confidence", ""),
                "topic_ok": topic_ok, "keywords_ok": keywords_ok,
                "manual_correct": "",
            })

    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nAutomatic score: {passed}/{len(cases)} passed both checks")
    print(f"Saved to {OUT}. Open it and fill in manual_correct (Y or N) for each row.")

if __name__ == "__main__":
    main()