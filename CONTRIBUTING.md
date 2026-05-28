# Contributing to LangGraph Workflow Engine

## Getting Started

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure
4. Run: `uvicorn backend.main:app --reload`

## Code Style

- Python: Follow PEP 8, use `ruff` for linting
- JS/React: Use functional components with hooks

## Testing

```bash
pytest tests/ -v
```

## Pull Request Process

1. Update tests for any new functionality
2. Ensure all tests pass
3. Run `make lint` before submitting
