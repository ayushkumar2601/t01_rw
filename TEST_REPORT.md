# Test Report

## Commands Executed
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Totals
- **Passed**: 18
- **Failed**: 0
- **Skipped**: 0
- **Blocked**: 0

## Integration Status
- The live integration test (`test_live_groq_call`) **passed** successfully against the live Groq API endpoint.
- End-to-end execution via `python -m src.main --input data/saas_company.json --output outputs/sample_report.json` succeeded and validated with zero errors.

## Coverage Breakdown
- **Schema Validation (`tests/test_schema.py`)**:
  - Valid report acceptance
  - Rejection of missing required fields
  - Rejection of extra/unsupported fields (`extra="forbid"`)
  - Strict type checking (rejection of booleans as ints, strict strings, rejecting empty strings)
  - Negative values rejected (negative budget, rank bounds 1–3)
  - List count validation (exactly 3 channels, exactly 4 roadmap phases)
- **Business Rules (`tests/test_business_rules.py`)**:
  - Valid report and company constraint verification
  - Channel ranks must equal [1, 2, 3] exactly and be unique
  - Channels must be distinct
  - Total channel budget must not exceed marketing budget
  - Excluded channels from company constraints are rejected
  - Channel prioritization score matches weighted formula
  - Primary bottleneck presence check
- **Groq SDK Handling & Integration (`tests/test_integration.py`)**:
  - Mocked successful API call & response parsing
  - Mocked malformed/invalid JSON rejection
  - Live Groq API invocation verification
- **Prompt Builder (`tests/test_prompt_builder.py`)**:
  - Prompt structure, system message, few-shot injection, and user company context verification

## Acceptance Checklist
- [x] Structural requirements strictly enforced (types, array sizes, extra key forbid).
- [x] Budget and company constraints verified at runtime.
- [x] Bounded retry and one corrective-generation attempt implemented via `src/main.py`.
- [x] Detailed schema tests ensuring no silent type coercion for critical elements.
- [x] Clean logs recorded per execution attempt in `logs/runs.jsonl`.
- [x] Live end-to-end inference tested and verified.
