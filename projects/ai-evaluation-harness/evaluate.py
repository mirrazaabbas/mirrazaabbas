"""Evaluation harness for comparing AI-system outputs against quality criteria."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Score:
    case_id: str
    keyword_recall: float
    groundedness: float
    concision: float
    overall: float


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def keyword_recall(output: str, required: list[str]) -> float:
    if not required:
        return 1.0
    text = output.lower()
    return sum(term.lower() in text for term in required) / len(required)


def groundedness(output: str, context: str) -> float:
    out = words(output)
    ctx = words(context)
    return len(out & ctx) / len(out) if out else 0.0


def concision(output: str, max_words: int) -> float:
    count = len(output.split())
    if count <= max_words:
        return 1.0
    return max(0.0, max_words / count)


def evaluate(case: dict) -> Score:
    recall = keyword_recall(case["output"], case.get("required_terms", []))
    ground = groundedness(case["output"], case.get("context", ""))
    concise = concision(case["output"], case.get("max_words", 120))
    overall = 0.45 * recall + 0.40 * ground + 0.15 * concise
    return Score(case["id"], round(recall, 3), round(ground, 3), round(concise, 3), round(overall, 3))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", nargs="?", default="sample_cases.json")
    args = parser.parse_args()
    cases = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    scores = [evaluate(case) for case in cases]
    report = {
        "cases": [asdict(s) for s in scores],
        "average_overall": round(sum(s.overall for s in scores) / len(scores), 3) if scores else 0,
        "pass_rate": round(sum(s.overall >= 0.65 for s in scores) / len(scores), 3) if scores else 0,
    }
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
