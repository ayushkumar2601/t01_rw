# LLM Brain - B2B SaaS Growth Strategy

## Overview
A Python-based CLI application that transforms synthetic SaaS business metrics into a prioritized B2B growth strategy and a 30-day execution plan using Groq and Llama 3.3 70B.

## Architecture
- **Prompt Builder**: Combines system prompts, procedures, and few-shot examples.
- **Groq Client**: Handles the API request for JSON generation.
- **Validator**: Strictly enforces schema adherence and business logic.
- **Logger**: Logs metadata and token usage.

## Setup
1. Create virtual environment and install requirements:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Add your GROQ_API_KEY
   ```

## Configuration
You can configure the model, request timeouts, output limits, and bounded retries in your `.env` file. If a validation error occurs, the system makes **one corrective-generation attempt**.
To change the requested model, update `GROQ_MODEL=llama-3.3-70b-versatile` inside `.env`.

## Usage
Run the CLI:
```bash
export PYTHONPATH="."
python -m src.main --input data/saas_company.json --output outputs/sample_report.json
```

## Testing
Run tests using pytest:
```bash
export PYTHONPATH="."
pytest tests/
```
To run the live integration test (requires a valid `GROQ_API_KEY`):
```bash
pytest -m integration tests/
```

## Logs
Logs for executions are kept at `logs/runs.jsonl`. No sensitive API keys or HTTP headers are logged.
