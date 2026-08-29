FROM python:3.12-slim

WORKDIR /app
COPY evaluate.py ./evaluate.py
COPY sample_cases.json ./sample_cases.json

CMD ["python", "evaluate.py", "sample_cases.json"]
