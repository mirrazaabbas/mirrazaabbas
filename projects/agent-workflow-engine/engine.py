"""Small production-style workflow engine for deterministic AI-agent orchestration."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable

StepFn = Callable[[dict[str, Any]], dict[str, Any]]

@dataclass
class Step:
    name: str
    fn: StepFn
    retries: int = 1

@dataclass
class RunEvent:
    step: str
    status: str
    attempt: int
    elapsed_ms: int
    detail: str = ""

@dataclass
class Workflow:
    steps: list[Step]
    events: list[RunEvent] = field(default_factory=list)

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        state = dict(state)
        for step in self.steps:
            last_error: Exception | None = None
            for attempt in range(1, step.retries + 2):
                started = time.perf_counter()
                try:
                    update = step.fn(dict(state))
                    if not isinstance(update, dict):
                        raise TypeError("Step must return a dictionary")
                    state.update(update)
                    elapsed = int((time.perf_counter() - started) * 1000)
                    self.events.append(RunEvent(step.name, "ok", attempt, elapsed))
                    last_error = None
                    break
                except Exception as exc:
                    elapsed = int((time.perf_counter() - started) * 1000)
                    self.events.append(RunEvent(step.name, "error", attempt, elapsed, str(exc)))
                    last_error = exc
            if last_error:
                state["workflow_status"] = "failed"
                state["failed_step"] = step.name
                state["error"] = str(last_error)
                return state
        state["workflow_status"] = "completed"
        return state


def classify(state):
    text = state["request"].lower()
    intent = "research" if any(x in text for x in ["research", "compare", "find"]) else "general"
    return {"intent": intent}


def plan(state):
    tasks = ["understand request", "collect relevant context", "produce structured result"]
    if state["intent"] == "research":
        tasks.insert(2, "compare evidence")
    return {"plan": tasks}


def execute(state):
    return {"result": {"summary": f"Workflow prepared for: {state['request']}", "tasks": state["plan"]}}


def main():
    workflow = Workflow([
        Step("classify", classify),
        Step("plan", plan),
        Step("execute", execute, retries=2),
    ])
    state = workflow.run({"request": "Research and compare AI assistant architectures"})
    print(json.dumps(state, indent=2))
    print("\nObservability events:")
    print(json.dumps([e.__dict__ for e in workflow.events], indent=2))

if __name__ == "__main__":
    main()
