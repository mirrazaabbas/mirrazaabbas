# AI Resume Keyword Matcher

A lightweight Python project that compares a resume with a job description, estimates keyword overlap, and highlights important terms that may be missing.

## Why I built it
Recruiters and applicant tracking systems often scan for role-relevant terminology. This project demonstrates practical text processing, keyword extraction, scoring logic, and command-line application design.

## Features
- Extracts useful keywords from job descriptions
- Compares them against resume content
- Calculates a simple match percentage
- Shows matched keywords
- Suggests missing terms to review and add only when they accurately reflect your experience
- Runs locally with no API key required

## Tech Stack
- Python
- Regular Expressions
- Collections / Counter
- Basic Natural Language Processing concepts

## Run locally
```bash
python app.py sample_resume.txt sample_job.txt
```

## Example output
```text
Resume Match Score: 63.3%

Matched keywords:
python, ai, automation, github

Suggested keywords to review/add where truthful:
apis, agents, data, analysis
```

## What this project demonstrates
Text preprocessing, keyword ranking, set comparison, scoring, CLI design, and responsible resume optimization.

## Future improvements
- TF-IDF keyword ranking
- Semantic similarity using embeddings
- Streamlit user interface
- PDF/DOCX resume parsing
- Skill-category detection

> Note: The score is a portfolio demonstration and is not intended to reproduce any specific commercial ATS algorithm.
