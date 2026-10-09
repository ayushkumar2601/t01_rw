# Test Report

## Commands Executed
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
GROQ_API_KEY=dummy PYTHONPATH=. pytest tests/
```

## Totals
- **Passed**: 17
- **Failed**: 0
- **Skipped**: 1
- **Blocked**: 0

## Integration Status
- The live integration test (`test_live_groq_call`) was **skipped** because no valid `GROQ_API_KEY` was provided. It is considered blocked by external credentials.

## Coverage
- **Schema Validation**: Tests ensure robust Pydantic type checking (rejecting booleans as ints, forbidding extra root/nested fields, rejecting empty strings and negative bounds).
- **Business Rules**: Tests enforce logic for correct channel ranks, exact phase counts, valid budget limits against the company profile, exclusion of forbidden channels, presence of evidence/rationale, and correctness of the prioritization score sum.
- **Groq SDK Handling**: Covered with mocks for JSON response extraction and proper `GroqClientError` mapping for invalid outputs.

## Acceptance Checklist
- [x] Structural requirements strictly enforced (types, array sizes, missing keys).
- [x] Budget and company constraints verified at runtime.
- [x] Bounded retry and one corrective-generation attempt implemented via `src/main.py`.
- [x] Detailed schema tests ensuring no silent type coercion for critical elements.
- [x] Clean logs recorded per execution attempt.
