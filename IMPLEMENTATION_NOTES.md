# Implementation Notes

- We combined `schemas/__init__.py` and `schemas/report_schema.py` for simplicity while respecting the directory structure.
- The `few_shot_examples.json` is loaded as an array of objects, containing both the input and the expected output for the few-shot interactions.
- Logging writes to `logs/runs.jsonl` to ensure all executions (successful or failed) are durably recorded in JSON Lines format.
- Output validation handles Pydantic's `ValidationError` as well as a suite of custom business logic validations (budget checks, lengths, day ranges).
- Tests will be added under `tests/` using `pytest`.
