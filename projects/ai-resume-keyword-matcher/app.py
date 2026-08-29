import argparse
import re
from collections import Counter
from pathlib import Path

STOPWORDS = {"the","and","a","an","to","of","in","for","with","on","is","are","as","at","be","by","or","from","that","this","we","you","your","our","will","have","has","using","use"}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#.-]*", text.lower())
    return [word for word in words if word not in STOPWORDS and len(word) > 1]


def keyword_counts(text: str) -> Counter[str]:
    return Counter(tokenize(text))


def match_resume(resume: str, job: str) -> dict[str, object]:
    resume_words = set(tokenize(resume))
    job_counts = keyword_counts(job)
    important = [word for word, _ in job_counts.most_common(30)]
    matched = [word for word in important if word in resume_words]
    missing = [word for word in important if word not in resume_words]
    score = round((len(matched) / len(important)) * 100, 1) if important else 0.0
    return {"score": score, "matched": matched, "missing": missing}


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"File is not valid UTF-8: {path}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare a resume with a job description using keyword overlap.")
    parser.add_argument("resume", type=Path)
    parser.add_argument("job_description", type=Path)
    args = parser.parse_args()
    try:
        resume = read_file(args.resume)
        job = read_file(args.job_description)
        if not resume.strip() or not job.strip():
            raise ValueError("Resume and job description must both contain text.")
    except ValueError as exc:
        parser.error(str(exc))
    result = match_resume(resume, job)
    print(f"\nResume Match Score: {result['score']}%")
    print("\nMatched keywords:")
    print(", ".join(result["matched"]) or "None")
    print("\nSuggested keywords to review/add where truthful:")
    print(", ".join(result["missing"][:15]) or "None")


if __name__ == "__main__":
    main()
