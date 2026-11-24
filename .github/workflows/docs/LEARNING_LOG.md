# FinDoc learning log

Newest entries at the top.

---

## 2026-11-24: M1 baseline (model only, no documents)

**What I did:** Ran the 20-question golden set against `/ask` using gpt-4.1-mini, with no documents. Graded every answer by hand against the source PDFs (FCAC down payment page, CMHC quick reference, OSFI B-20 letter).

**Result:**
- **Manual score: 13/20**
- Topic classification: 20/20 (including both off-topic refusals)
- Passed both automatic checks (topic + keywords): 12/20

**What went wrong (7 answers):**
- **Out-of-date rules:**
  - q10: said 25 years only, missed the 30-year CMHC Home Start option
  - q12: gave an older qualifying rate instead of "contract + 2% or 5.25%"
  - q18: said $1M, but the current limit is under $1.5M, and it didn't notice the FCAC vs CMHC conflict
- **Wrong document details:**
  - q07: named British Columbia instead of Ontario, and said the tax can be added to the mortgage (it can't)
  - q14: said 85% LTV instead of 80%
  - q15: said June 1, 2021 instead of January 1, 2018
- **Opposite of the regulation:**
  - q16: said banks must re-apply the qualifying rate at renewal; B-20 says they are not expected to

**Other observations:**
- The keyword check marked one partly correct answer (q09) as failed. It's a rough filter; manual grading is the real score for now.
- Confidence on the wrong answers: <check the CSV: were any marked "high"?>

**Decision / next step:** The mistakes are mostly out-of-date or document-specific facts, which is what answering from the PDFs should fix. In M2: build document Q&A with citations, re-run this golden set, and compare against 13/20.
