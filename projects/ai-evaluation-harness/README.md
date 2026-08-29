# AI Evaluation Harness

A compact benchmark framework for evaluating AI-system outputs with repeatable, measurable criteria instead of relying only on subjective inspection.

## What it evaluates

- **Keyword recall** — whether required concepts are present
- **Groundedness proxy** — lexical support from supplied source context
- **Concision** — whether the response stays within an expected length
- **Weighted overall score**
- **Dataset-level pass rate**

## Run

```bash
python evaluate.py sample_cases.json
```

The benchmark cases are plain JSON, making it easy to add regression tests as prompts, retrieval logic, or models change.

## Why evaluation matters

A serious AI application needs a feedback loop. Prompt changes and model upgrades can improve one behavior while silently degrading another. An evaluation harness provides a repeatable way to compare versions and catch regressions.

## Architecture

`Benchmark Dataset → Metric Functions → Per-case Scores → Aggregate Report → Regression Decision`

## Production extensions

- Semantic similarity with embeddings
- LLM-as-a-judge with calibrated rubrics
- Citation correctness
- Hallucination/factuality checks
- Cost and latency tracking
- Baseline-vs-candidate comparisons
- CI quality gates

## Skills demonstrated

Python · AI Evaluation · LLMOps · Benchmarking · Quality Engineering · JSON · Metrics Design
