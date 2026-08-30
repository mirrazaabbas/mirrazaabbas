# Integrated AI System Evidence

This portfolio is designed so the three flagship engineering projects can interoperate through a small, versioned JSON boundary rather than depending on each other's internal Python modules.

## System flow

```text
RAG Knowledge Assistant
  ├─ source-grounded retrieval
  ├─ PostgreSQL / pgvector path
  ├─ citations + ranking evidence
  └─ portfolio-evidence/v1
             ↓
Agent Workflow Engine
  ├─ permission-scoped RAG HTTP tool
  ├─ retries + timeout controls
  ├─ approval / idempotency / checkpoints
  ├─ runtime telemetry
  └─ portfolio-evidence/v1
             ↓
AI Evaluation Harness
  ├─ answer token F1
  ├─ recall@k / reciprocal rank / nDCG@k
  ├─ citation precision / recall
  ├─ tool-call accuracy
  └─ pass/fail quality evidence
```

## Why the contract matters

`portfolio-evidence/v1` is deliberately plain JSON-compatible data. This keeps the systems loosely coupled and makes evidence portable between services, CI jobs, files, or future APIs.

Typical fields include:

- `schema_version`
- `producer`
- `query`
- `output`
- `retrieved_ids`
- `citations`
- `context`
- retrieval ranks and scores
- tool-call metadata
- latency when measured
- agent runtime events when produced by the workflow engine

No credentials are stored in the evidence contract.

## Verified implementation locations

### RAG Knowledge Assistant

Repository: https://github.com/mirrazaabbas/rag-knowledge-assistant

- `integration_contract.py` builds and validates the shared evidence format.
- CI validates the evidence contract in addition to the existing pgvector, Docker, benchmark, prompt-injection, and OpenTelemetry/Jaeger checks.

### Agent Workflow Engine

Repository: https://github.com/mirrazaabbas/agent-workflow-engine

- `adapters.py` contains an OpenAI-compatible model adapter and HTTP adapter for the RAG `/answer` endpoint.
- `portfolio_pipeline.py` executes a permission-scoped RAG call through the async runtime and emits evaluator-ready evidence.
- `telemetry.py` converts runtime events to JSON and can export them through an OpenTelemetry-compatible tracer interface.
- CI tests adapters through injected transports, so public CI requires no model secrets.

### AI Evaluation Harness

Repository: https://github.com/mirrazaabbas/ai-evaluation-harness

- `portfolio_bridge.py` validates and evaluates `portfolio-evidence/v1` records.
- `sample_portfolio_run.json` and `sample_portfolio_expected.json` provide a credential-free integration example.
- CI executes the bridge and checks retrieval, citation, answer, and tool-call evaluation behavior.

## Engineering properties demonstrated

| Property | Evidence |
|---|---|
| Loose coupling | Versioned JSON contract instead of cross-repo implementation imports |
| Grounding | Retrieved source IDs, context, citations, ranks, and scores preserved |
| Reliability | Retries, timeouts, checkpoint/resume, idempotency, permission scopes |
| Observability | Runtime events plus OpenTelemetry-compatible export; RAG has live OTLP→Jaeger CI verification |
| Evaluation | Deterministic answer, retrieval, citation, tool-call, regression, latency/cost metrics |
| Security boundaries | Environment-based credentials, prompt-injection boundaries, permission-scoped external tool use |
| Reproducibility | Credential-free integration fixtures and automated CI |
| Maintenance | Weekly Dependabot updates for Python and GitHub Actions on the portfolio engineering repos |

## Accuracy boundaries

This portfolio distinguishes between implemented evidence and future extensions:

- The OpenAI-compatible agent adapter is real code and is tested with an injected HTTP transport; public CI does not perform billable external model calls.
- The RAG project has real pgvector and OTLP/Jaeger integration tests, but its deterministic CI benchmark is not presented as a commercial embedding-model quality benchmark.
- The Evaluation Harness metrics are deterministic and reproducible. It does not claim semantic factuality or an LLM-as-a-judge unless such an evaluator is explicitly implemented and tested.
- The Agent Workflow Engine is not presented as a distributed autonomous-agent platform or MCP server. Distributed workers, database-backed workflow state, and MCP remain future extensions.

## Recruiter review path

For a quick technical review:

1. Start with the RAG Knowledge Assistant architecture and CI evidence.
2. Inspect Agent Workflow Engine `runtime.py`, `adapters.py`, and `portfolio_pipeline.py`.
3. Inspect AI Evaluation Harness `advanced_metrics.py` and `portfolio_bridge.py`.
4. Review the CI workflows to see which claims are automatically verified.

The goal is to demonstrate not just AI features, but the engineering around them: interfaces, failure handling, observability, validation, security boundaries, and measurable quality.
