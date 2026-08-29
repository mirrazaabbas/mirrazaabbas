# Security Policy

## Reporting a vulnerability

Please do not publish secrets, API keys, access tokens, personal data, or exploitable security details in a public issue.

If you discover a vulnerability in one of the portfolio projects, open a GitHub issue with a high-level description that does not include credentials or sensitive exploit data. Include the affected project, expected behavior, observed behavior, and reproduction steps that are safe to share publicly.

## Security principles used in this repository

- Secrets belong in environment variables, never source control.
- `.env` files are ignored; `.env.example` files may document variable names only.
- Inputs should be validated before processing.
- File paths and uploads should be treated as untrusted input.
- AI-agent tools should use least-privilege permissions.
- Retrieved content in RAG systems should be treated as untrusted data, not instructions.
- Logs should never contain credentials or private user data.
- High-impact automated actions should support human approval.

## Supported code

The `main` branch is the actively maintained portfolio branch.
