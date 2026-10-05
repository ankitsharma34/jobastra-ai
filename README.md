# JobAstra AI

JobAstra AI is the independent AI service of the [**JobAstra**](https://github.com/ankitsharma34/JobAstra) platform.

It is responsible for handling AI-powered features such as job matching, job-fit analysis, personalized application generation, and agentic workflows.

The service is built separately from the main JobAstra application so that AI logic, models, tools, and workflows can evolve independently.

## Tech Stack

- Python
- FastAPI
- Pydantic
- uv
- Ruff
- pytest

## Development

Install dependencies:

```bash
uv sync
```

Run the development server:

```bash
uv run uvicorn jobastra_ai.main:app --app-dir src --reload
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Format code:

```bash
uv run ruff format .
```
