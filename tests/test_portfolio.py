from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class PortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resume = load_module("resume_matcher", "projects/ai-resume-keyword-matcher/app.py")
        cls.prompt = load_module("prompt_lab", "projects/prompt-engineering-lab/prompt_lab.py")
        cls.csvmod = load_module("csv_analyzer", "projects/csv-insight-analyzer/analyzer.py")
        cls.rag = load_module("rag_assistant", "projects/rag-knowledge-assistant/app.py")
        cls.agent = load_module("agent_engine", "projects/agent-workflow-engine/engine.py")
        cls.evaluator = load_module("ai_evaluator", "projects/ai-evaluation-harness/evaluate.py")

    def test_resume_matcher(self):
        result = self.resume.match_resume(
            "Python automation prompt engineering APIs",
            "Need Python, APIs, automation and data analysis skills",
        )
        self.assertGreater(result["score"], 0)
        self.assertIn("python", result["matched"])

    def test_resume_file_handling(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resume.txt"
            path.write_text("Python AI automation", encoding="utf-8")
            self.assertIn("Python", self.resume.read_file(path))
            with self.assertRaises(ValueError):
                self.resume.read_file(Path(tmp) / "missing.txt")

    def test_prompt_library_and_generation(self):
        prompts = self.prompt.load_prompts()
        self.assertGreaterEqual(len(prompts), 3)
        first = prompts[0]
        values = {variable: "test value" for variable in first["variables"]}
        output = self.prompt.build_prompt(first, values)
        self.assertNotIn("{", output)
        self.assertIn("test value", output)
        with self.assertRaises(ValueError):
            self.prompt.build_prompt(first, {})
        bad_values = {variable: "" for variable in first["variables"]}
        with self.assertRaises(ValueError):
            self.prompt.build_prompt(first, bad_values)

    def test_prompt_library_validation_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            invalid = Path(tmp) / "bad.json"
            invalid.write_text("{not-json", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.prompt.load_prompts(invalid)
            empty = Path(tmp) / "empty.json"
            empty.write_text("[]", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.prompt.load_prompts(empty)

    def test_csv_analyzer(self):
        rows = [
            {"region": "North", "product": "AI", "revenue": "100"},
            {"region": "South", "product": "AI", "revenue": "200"},
        ]
        report = self.csvmod.analyze_sales(rows)
        self.assertEqual(report["rows"], 2)
        self.assertEqual(report["total_revenue"], 300.0)
        self.assertEqual(report["top_region"][0], "South")
        with self.assertRaises(ValueError):
            self.csvmod.analyze_sales([])
        with self.assertRaises(ValueError):
            self.csvmod.to_float("not-a-number", 2)
        with self.assertRaises(ValueError):
            self.csvmod.analyze_sales([{"region": "", "product": "AI", "revenue": "10"}])

    def test_csv_schema_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.csv"
            bad.write_text("region,revenue\nNorth,10\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.csvmod.load_rows(bad)
            with self.assertRaises(ValueError):
                self.csvmod.load_rows(Path(tmp) / "missing.csv")

    def test_rag_retrieval(self):
        text_a = "RAG retrieves trusted context for grounded answers"
        text_b = "Python is a programming language"
        chunks = [
            self.rag.Chunk("a.md", text_a, self.rag.Counter(self.rag.tokens(text_a))),
            self.rag.Chunk("b.md", text_b, self.rag.Counter(self.rag.tokens(text_b))),
        ]
        results = self.rag.search(chunks, "grounded retrieval context", 1)
        self.assertEqual(results[0][1].source, "a.md")
        self.assertGreater(results[0][0], 0)
        self.assertEqual(self.rag.search([], "query", 1), [])
        with self.assertRaises(ValueError):
            self.rag.search(chunks, "query", 0)
        with self.assertRaises(ValueError):
            self.rag.search(chunks, "!!!", 1)
        with self.assertRaises(ValueError):
            self.rag.chunk_text("hello", 0, 0)
        with self.assertRaises(ValueError):
            self.rag.chunk_text("hello", 5, 5)
        self.assertEqual(self.rag.vector(self.rag.Counter(), {}), {})

    def test_rag_document_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            with self.assertRaises(FileNotFoundError):
                self.rag.load_corpus(missing)

    def test_agent_workflow_and_event_reset(self):
        workflow = self.agent.Workflow([
            self.agent.Step("classify", self.agent.classify),
            self.agent.Step("plan", self.agent.plan),
            self.agent.Step("execute", self.agent.execute),
        ])
        first = workflow.run({"request": "Research AI agents"})
        self.assertEqual(first["workflow_status"], "completed")
        self.assertEqual(len(workflow.events), 3)
        workflow.run({"request": "Build an assistant"})
        self.assertEqual(len(workflow.events), 3)

    def test_agent_validation_and_failure(self):
        with self.assertRaises(ValueError):
            self.agent.Step("", self.agent.classify)
        with self.assertRaises(ValueError):
            self.agent.Step("x", self.agent.classify, retries=-1)
        with self.assertRaises(ValueError):
            self.agent.classify({"request": ""})
        with self.assertRaises(ValueError):
            self.agent.plan({})

        def fail(_state):
            raise RuntimeError("boom")

        workflow = self.agent.Workflow([self.agent.Step("fail", fail, retries=1)])
        result = workflow.run({"request": "test"})
        self.assertEqual(result["workflow_status"], "failed")
        self.assertEqual(result["failed_step"], "fail")
        self.assertEqual(len(workflow.events), 2)

    def test_evaluation_harness(self):
        case = {
            "id": "case-1",
            "context": "RAG retrieves source context before generation",
            "output": "RAG retrieves source context before generation",
            "required_terms": ["RAG", "source context"],
            "max_words": 20,
        }
        score = self.evaluator.evaluate(case)
        self.assertEqual(score.keyword_recall, 1.0)
        self.assertEqual(score.groundedness, 1.0)
        self.assertGreaterEqual(score.overall, 0.9)
        self.assertEqual(self.evaluator.keyword_recall("anything", []), 1.0)
        self.assertEqual(self.evaluator.groundedness("", "context"), 0.0)
        self.assertLess(self.evaluator.concision("one two three four", 2), 1.0)

    def test_sample_evaluation_dataset(self):
        path = ROOT / "projects/ai-evaluation-harness/sample_cases.json"
        cases = self.evaluator.load_cases(path)
        report = self.evaluator.build_report(cases)
        self.assertEqual(len(report["cases"]), 2)
        self.assertGreaterEqual(report["pass_rate"], 0.5)

    def test_sample_csv_file(self):
        path = ROOT / "projects/csv-insight-analyzer/sample_sales.csv"
        report = self.csvmod.analyze_sales(self.csvmod.load_rows(path))
        self.assertEqual(report["rows"], 10)
        self.assertGreater(report["total_revenue"], 0)

    def test_sample_rag_docs(self):
        docs = ROOT / "projects/rag-knowledge-assistant/sample_docs"
        corpus = self.rag.load_corpus(docs)
        results = self.rag.search(corpus, "How can AI agents reduce unsupported claims?", 1)
        self.assertTrue(results)
        self.assertGreaterEqual(results[0][0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
