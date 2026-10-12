# Prompt Architecture — LLM Brain B2B Growth Strategy

## 1. Project Objective and Scope
The goal of this system is to transform raw synthetic B2B SaaS metrics into a prioritized, actionable growth strategy and 30-day "systems, not campaigns" execution plan.
Instead of relying on free-form conversational LLM output, this architecture enforces a deterministic, multi-layered prompting engine coupled with strict schema validation to eliminate hallucinations, enforce domain constraints, and guarantee machine-readable JSON reports.

---

## 2. Multi-Layered Prompt Stack Architecture

The prompt is assembled sequentially into an OpenAI/Groq-compatible message array with five distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. SYSTEM PROMPT: Persona, Constraints & Objective          │
├─────────────────────────────────────────────────────────────┤
│ 2. REASONING PROCEDURE: 10-Step Chain-of-Thought Rubric     │
├─────────────────────────────────────────────────────────────┤
│ 3. OUTPUT CONTRACT: Injected Pydantic JSON Schema           │
├─────────────────────────────────────────────────────────────┤
│ 4. FEW-SHOT EXAMPLES: User input -> Assistant output pairs   │
├─────────────────────────────────────────────────────────────┤
│ 5. CONTEXT INJECTION: Actual Company Metrics (User message) │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: System Persona & Behavioral Constraints
Located in `prompts/system.md`. Defines the expert identity and fundamental guardrails:

```markdown
You are a senior B2B SaaS growth strategist and growth-operations architect with expertise in retention, acquisition, and revenue operations.

Your goal is to optimize for sustainable, measurable growth rather than vanity metrics.

Follow these strict constraints:
1. Diagnose the most significant business bottlenecks before proposing solutions.
2. Rank exactly three channels based on impact, feasibility, cost, and time to learn.
3. Prefer repeatable systems over isolated marketing campaigns.
4. Make every action measurable and assign an owner.
5. Separate facts, assumptions, and proposed targets.
6. Avoid invented benchmarks, unsupported causal claims, and guaranteed outcomes.
7. Return only the requested JSON object.
8. Never add keys outside the specified schema.
9. Ensure each channel's priority_score strictly equals: (0.35 * score_impact) + (0.25 * score_fit) + (0.20 * score_feasibility) + (0.10 * score_learning_speed) + (0.10 * score_cost_efficiency).
```

### Layer 2: Chain-of-Thought & Reasoning Procedure
Located in `prompts/strategy_procedure.md`. Instructs the model step-by-step on how to analyze metrics, identify bottlenecks, score channels mathematically, and build a systems-first roadmap:

```markdown
Internal Problem-Solving Procedure:
1. Assess the supplied business metrics (acquisition, conversion, retention, monetization).
2. Identify the most important bottlenecks and cite the exact input metrics supporting each finding.
3. Generate plausible growth-channel candidates.
4. Score candidates across the 5 evaluation criteria (each scored 0 to 100):
   - score_impact (weight: 35% / 0.35)
   - score_fit (weight: 25% / 0.25)
   - score_feasibility (weight: 20% / 0.20)
   - score_learning_speed (weight: 10% / 0.10)
   - score_cost_efficiency (weight: 10% / 0.10)
   Tip: Choose clean round numbers (multiples of 10 or 20 like 80, 70, 60) for sub-scores so arithmetic is exact.
5. Calculate priority_score with strict mathematical accuracy:
   priority_score = round((0.35 * score_impact) + (0.25 * score_fit) + (0.20 * score_feasibility) + (0.10 * score_learning_speed) + (0.10 * score_cost_efficiency), 2)
   CRITICAL: priority_score MUST strictly match this formula. Verify your arithmetic before outputting.
6. Select exactly three channels.
7. Design a repeatable system for each selected channel.
8. Build a four-week execution roadmap.
9. Assign an owner, deadline (due_day 1-30), success metric, and deliverable to every task.
10. Check budgets, dependencies, assumptions, schema requirements, and business constraints before returning the report.
```

### Layer 3: Output Schema Injection
The Pydantic schema defined in `schemas/report_schema.py` is dynamically converted to a standard JSON Schema (`ReportSchema.model_json_schema()`) and appended directly to the system prompt. This ensures the model receives unambiguous field names, data types, constraints, and nesting hierarchies.

### Layer 4: Few-Shot In-Context Learning
Located in `prompts/few_shot_examples.json`. Injects a paired `user` (synthetic input) and `assistant` (complete valid JSON report) message before the real user data. This demonstrates:
- The tone, depth, and precision required in rationales and systems.
- Exact compliance with the 4-phase weekly structure (`due_day` 1 to 30).
- Strict adherence to JSON formatting without introductory text or markdown ticks.

### Layer 5: Context Injection (Synthetic SaaS Company Data)
Located in `data/saas_company.json`. The runtime injects the company profile as the final `user` message. Isolating the facts from the system rules guarantees that company parameters cannot override behavioral constraints.

```json
{
  "company": {
    "name": "FlowPilot",
    "description": "Workflow automation SaaS for B2B service teams",
    "stage": "early_growth",
    "business_model": "B2B SaaS",
    "target_market": "SMB and mid-market",
    "primary_icp": "Operations leaders at 20-200 person companies",
    "average_contract_value_usd": 2400
  },
  "metrics": {
    "mrr_usd": 18000,
    "monthly_churn_rate_pct": 8.5,
    "monthly_website_visitors": 4500,
    "monthly_inbound_leads": 35,
    "lead_to_customer_conversion_pct": 2.0,
    "customer_acquisition_cost_usd": 900,
    "monthly_marketing_budget_usd": 3000,
    "net_revenue_retention_pct": 88
  },
  "constraints": {
    "team_size": 3,
    "engineering_capacity": "limited",
    "sales_capacity": "founder_led",
    "implementation_window_days": 30,
    "existing_channels": ["organic_search", "linkedin"],
    "excluded_channels": ["large_paid_advertising_campaigns"]
  }
}
```

---

## 3. Strict Schema & Anti-Hallucination Enforcement

Hallucinations and structural drift are prevented at multiple levels:

1. **In-Prompt Structural Negative Constraints**:
   - `Never add keys outside the specified schema.`
   - `Return only the requested JSON object.`
2. **Groq API JSON Mode**:
   - `response_format={"type": "json_object"}` forces syntactically valid JSON syntax.
3. **Pydantic Strict Validation (`extra="forbid"`)**:
   - All models (`ExecutiveSummary`, `PrioritizedGrowthChannel`, `Action`, `WeeklyPhase`, `ReportSchema`) enforce `ConfigDict(extra="forbid", strict=True)`.
   - String fields enforce `min_length=1` to reject empty strings.
   - Numeric fields enforce strict types (`StrictInt`, `StrictFloat`) to prevent silent boolean-to-integer coercion.
   - Lists enforce exact counts: `prioritized_growth_channels` requires exactly 3 items; `action_plan_30_days` requires exactly 4 weekly phases.
4. **Deterministic Business Rule Validation (`src/validator.py`)**:
   - **Ranks**: Verifies channel ranks are exactly `[1, 2, 3]` and unique.
   - **Uniqueness**: Ensures all 3 channel names are distinct.
   - **Weeks & Days**: Verifies roadmap weeks are `[1, 2, 3, 4]` and task `due_day` falls between 1 and 30.
   - **Budget Cap**: Verifies the sum of channel budgets does not exceed `monthly_marketing_budget_usd`.
   - **Excluded Channels**: Enforces company constraints (e.g., rejects channels matching excluded channel patterns).
   - **Mathematical Audit**: Recalculates the weighted priority score from the 5 scoring factors and verifies consistency within ±0.1 tolerance.

---

## 4. Failure Handling & Bounded Self-Correction

If validation fails, the system executes a bounded recovery flow:
1. Catches specific Groq API errors (`AuthenticationError`, `RateLimitError`, `APITimeoutError`, `APIConnectionError`, `APIError`) with exponential backoff retries.
2. If the LLM generates valid JSON that fails Pydantic schema or business rule validation, `src/main.py` performs **one corrective re-generation attempt**.
3. It appends the exact list of validation errors back to the conversation as feedback and asks for a corrected JSON object.
4. If the corrective attempt also fails, execution terminates cleanly with an exit code of 1 and records the failure in `logs/runs.jsonl`.

---

## 5. Execution Logging & Audit Trail
Every run (successful or failed) appends an audit record to `logs/runs.jsonl` with:
- `run_id` (UUID)
- `timestamp` (ISO-8601 UTC)
- `prompt_version`
- `requested_model` and `returned_model`
- `input_hash` (SHA-256 of input content)
- `status` (`success`, `validation_failed`, or `error`)
- `latency` (seconds)
- `token_usage` (prompt, completion, total, and reasoning tokens)
- `validation_errors` (if any)
- `output_path`
