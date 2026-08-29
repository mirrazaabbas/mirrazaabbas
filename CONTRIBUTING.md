# Contributing

Thanks for checking out this portfolio repository.

## Development workflow

1. Create a feature branch from `main`.
2. Keep each change focused and use descriptive commit messages.
3. Run the full test suite before opening a pull request.
4. Explain what changed, why it changed, and how it was tested.
5. Do not commit secrets, generated credentials, private datasets, or `.env` files.

## Local checks

```bash
python -m compileall -q projects tests
python tests/test_portfolio.py
```

The GitHub Actions workflow also runs smoke tests across Python 3.10, 3.11, and 3.12.

## Commit style

Prefer specific messages such as:

- `Add retrieval input validation`
- `Improve workflow retry handling`
- `Add evaluation regression cases`

Avoid vague messages such as `update`, `fix`, or `changes`.

## Pull request checklist

- [ ] Code compiles
- [ ] Tests pass
- [ ] New behavior is covered by tests where practical
- [ ] README/docs are updated
- [ ] No secrets or private data are included
- [ ] Error handling is clear and user-friendly
