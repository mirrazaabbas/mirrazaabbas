# Prompt Engineering Lab

A small Python toolkit for generating structured, reusable prompts from configurable templates.

## Why I built it
Prompt engineering is more useful when prompts are consistent, reusable, and designed around clear roles, inputs, constraints, and output formats. This project turns those ideas into a simple working CLI tool.

## Features
- JSON-based reusable prompt templates
- Interactive command-line interface
- Variable substitution for different tasks
- Templates for research, content creation, and data analysis
- No API key required

## Tech Stack
- Python
- JSON
- Prompt Engineering
- CLI application design

## Run locally
```bash
python prompt_lab.py
```

Choose a template, enter the requested values, and the application produces a structured prompt ready to use with an AI assistant.

## Prompt design principles demonstrated
- Clear role definition
- Explicit user goal
- Context and audience
- Constraints against unsupported claims
- Defined output structure
- Reusable prompt variables

## Future improvements
- Add a Streamlit interface
- Save generated prompts to Markdown
- Add prompt versioning and evaluation
- Connect optional LLM APIs
- Add more templates for coding, planning, and career workflows
