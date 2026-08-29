# Agent Workflow Engine

A lightweight orchestration engine for multi-step AI-agent workflows. It models an agent as explicit, observable steps instead of one opaque prompt, with shared state, retries, failure handling, and execution telemetry.

## Architecture

`Request → Intent Classification → Planning → Execution → Structured Result`

Each step receives workflow state and returns a state update. The engine records status, attempts, latency, and errors for every step.

## Features

- Composable workflow steps
- Shared typed state pattern
- Per-step retry policies
- Graceful failure state
- Execution event/latency logging
- Deterministic example agent pipeline
- Standard-library implementation

## Run

```bash
python engine.py
```

## Why this is an advanced portfolio project

Agent systems become difficult to debug when planning, tools, memory, and generation are mixed together. This project demonstrates orchestration concepts used in larger agent frameworks while keeping the implementation small enough to understand end-to-end.

## Production extensions

- Async/parallel tool execution
- Conditional graph routing
- Persistent checkpoints
- Human approval nodes
- LLM/tool adapters
- OpenTelemetry tracing
- Workflow evaluation and cost tracking

## Skills demonstrated

Python · AI Agents · Workflow Orchestration · State Machines · Reliability · Observability · Software Architecture
