import re
import sys
from collections import Counter

STOPWORDS = {
    "the", "and", "a", "an", "to", "of", "in", "for", "with", "on", "is", "are",
    "as", "at", "be", "by", "or", "from", "that", "this", "we", "you", "your",
    "our", "will", "have", "has", "using", "use"
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{1,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def keyword_counts(text: str) -> Counter:
    return Counter(tokenize(text))


def match_resume(resume: str, job: str) -> dict:
    resume_words = set(tokenize(resume))
    job_counts = keyword_counts(job)

    important = [word for word, _ in job_counts.most_common(30)]
    matched = [word for word in important if word in resume_words]
    missing = [word for word in important if word not in resume_words]

    score = round((len(matched) / len(important)) * 100, 1) if important else 0.0
    return {"score": score, "matched": matched, "missing": missing}


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python app.py <resume.txt> <job_description.txt>")
        raise SystemExit(1)

    result = match_resume(read_file(sys.argv[1]), read_file(sys.argv[2]))

    print(f"\nResume Match Score: {result['score']}%")
    print("\nMatched keywords:")
    print(", ".join(result["matched"]) or "None")
    print("\nSuggested keywords to review/add where truthful:")
    print(", ".join(result["missing"][:15]) or "None")


if __name__ == "__main__":
    main()
