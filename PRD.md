# Technical PRD — LLM Brain Prompting Architecture

Task 01 · B2B Growth Strategy Intelligence Engine · Version 1.0 · October 2026

The goal is to build a reliable, schema-enforced LLM pipeline that transforms synthetic SaaS business metrics into a prioritized B2B growth strategy and a 30-day execution plan. This is not just a chatbot: it is a small, testable AI system with structured prompting, constrained JSON generation, validation, and execution logs.

The deliverable should demonstrate four engineering skills: prompt architecture, LLM API integration, structured output enforcement, and automated validation.

## 1. Product overview

## LLM Brain

Input → Context → Reasoning → Structured report → Validation

Synthetic SaaS Business Data

MRR · Churn · Leads · CAC · Conversion · ICP

Prompt Orchestrator

System prompt + context + strategy instructions + output contract

Groq API — Llama 3.3 70B

Structured generation using JSON Schema where supported

Validator

JSON parsing, schema, types and business rules

Report Output

Validated JSON + reproducible logs

### 1.1 Problem statement

B2B SaaS founders often have fragmented growth data but lack a clear, prioritized operating plan. A general-purpose LLM may return generic advice, inconsistent recommendations, invalid JSON, unsupported assumptions, or action plans that lack measurable outcomes.

The LLM Brain must convert a defined business context into an actionable report while enforcing a fixed output contract.

### 1.2 Product objective

Build a Python-based command-line application that:

* Accepts structured SaaS metrics and business context.

* Uses a layered prompt architecture to generate a growth strategy.

* Prioritizes exactly three growth channels using business evidence.

* Produces a 30-day systems-oriented execution roadmap.

* Returns a machine-readable JSON object that conforms to a strict schema.

* Logs the request, response, validation outcome, and execution metadata.

### 1.3 Success criteria

| Metric              | Acceptance target                               |
| ------------------- | ----------------------------------------------- |
| JSON validity       | 100% of accepted reports parse successfully     |
| Schema compliance   | 100% of accepted reports pass strict validation |
| Growth channels     | Exactly 3, ranked 1–3                           |
| Roadmap             | 30 days, grouped into 4 weekly phases           |
| Hallucinated fields | No additional keys accepted                     |
| Reproducibility     | Inputs, prompt version, and output logged       |
| Failure handling    | Invalid outputs rejected and handled gracefully |

These are acceptance targets, not assumed results. They must be measured during testing.

## 2. Functional requirements

Priority: P0 = required for submission · P1 = recommended improvement

FR-01

Business context ingestion

P0

Load a synthetic SaaS company profile from a JSON configuration file.

FR-02

Layered prompt orchestration

P0

Combine system instructions, business context, strategic reasoning instructions, few-shot examples, and output requirements.

FR-03

Structured LLM generation

P0

Call Groq using the configured Llama model and JSON Schema constrained output, where supported.

FR-04

Strict output validation

P0

Reject malformed JSON, missing fields, additional keys, invalid types, and incorrect channel or roadmap counts.

FR-05

Growth strategy generation

P0

Produce an executive summary, three ranked channels, and a 30-day systems-first action plan.

FR-06

Execution logging

P0

Record input, prompt version, model, response, latency, token usage when available, and validation result.

FR-07

Failure handling

P0

Handle API errors, timeouts, rate limits, malformed responses, and validation failures without returning invalid reports.

FR-08

Automated testing

P0

Run schema tests, business-rule tests, prompt checks, and a live API integration test.

FR-09

Retry and repair

P1

Optionally retry once with validation errors as corrective feedback, with a strict retry limit.

FR-10

Human-readable reporting

P1

Optionally render the validated JSON as Markdown for founders and growth teams.

## 3. Non-functional requirements

* Reliability: No invalid report may be treated as successful.

* Maintainability: Keep prompts, schemas, configuration, orchestration, and validation in separate files.

* Security: Read the Groq API key from an environment variable. Never log secrets.

* Observability: Every run must have a unique ID, timestamps, and a clear status.

* Cost control: Limit output tokens, API retries, and unnecessary calls.

* Portability: Run locally on Python 3.11+ without a database or frontend.

* Privacy: Use synthetic company data for the submitted demonstration; avoid sending real customer PII.

## 4. Technology stack

| Component         | Technology                | Purpose                                            |
| ----------------- | ------------------------- | -------------------------------------------------- |
| Runtime           | Python 3.11+              | Application and orchestration                      |
| LLM provider      | Groq API                  | Hosted inference                                   |
| Model             | `llama-3.3-70b-versatile` | Strategy generation, subject to model availability |
| API client        | `groq`                    | API communication                                  |
| Schema validation | `pydantic`                | Strict typed models and extra-field rejection      |
| Configuration     | `python-dotenv`           | Local environment variables                        |
| Logging           | Python `logging` + JSONL  | Persistent execution records                       |
| Testing           | `pytest`                  | Automated validation and integration tests         |
| Version control   | Git                       | Track prompt and code changes                      |

Important implementation detail: Verify that the selected Groq model supports the required structured-output mode at implementation time. If JSON Schema constrained output is supported, use it. Otherwise, request JSON mode if available and rely on strict local validation. Neither prompt instructions nor JSON mode alone replace application-side schema validation.

## 5. Input specification and synthetic dataset

The initial version uses one fixed synthetic company profile. Later versions may support command-line overrides or a JSON input file.

Example: `data/saas_company.json`

JSON

```
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
    "existing_channels": [
      "organic_search",
      "linkedin"
    ],
    "excluded_channels": [
      "large_paid_advertising_campaigns"
    ]
  }
}
```

All figures are illustrative, not real company data. Treat them as unverified business inputs rather than independently established facts.

### Required input-handling rules

1. Validate the input data before calling the LLM.

2. Distinguish supplied metrics from assumptions and proposed targets.

3. Do not allow the model to invent additional company metrics.

4. Flag missing information as a limitation instead of fabricating values.

5. Ensure recommendations respect the budget, team size, and implementation window.

## 6. Prompting architecture

The prompt engine is the core of the project. It should separate instructions by purpose rather than place everything in a single unstructured prompt.

Layer 1 — System prompt

Defines the strategist persona, objectives, hard constraints, evidence rules, and JSON-only output contract.

Layer 2 — Context injection

Injects validated company metrics, ICP, business model, constraints, and known limitations as structured data.

Layer 3 — Strategy procedure

Requires evidence-based diagnosis, channel scoring, prioritization, sequencing, and measurable action design.

Layer 4 — Few-shot examples

Demonstrates how a sample business problem maps to a valid, correctly structured strategic recommendation.

Layer 5 — Output contract

Defines the JSON schema, required fields, enums, lengths, exact counts, and prohibition on additional properties.

### 6.1 System prompt requirements

The system prompt must instruct the LLM to:

* Act as a senior B2B SaaS growth strategist with expertise in retention, acquisition, and revenue operations.

* Optimize for sustainable, measurable growth rather than vanity metrics.

* Diagnose the most significant business bottlenecks before proposing solutions.

* Rank exactly three channels based on impact, feasibility, cost, and time to learn.

* Prefer repeatable systems over isolated marketing campaigns.

* Make every action measurable and assign an owner.

* Separate facts, assumptions, and proposed targets.

* Avoid invented benchmarks, unsupported causal claims, and guaranteed outcomes.

* Return only the requested JSON object.

* Never add keys outside the specified schema.

### 6.2 Chain-of-thought handling

The prompt should specify a reasoning procedure, not require the model to expose private internal chain-of-thought.

The internal procedure should cover:

1. Diagnose acquisition, conversion, retention, and monetization.

2. Identify the strongest evidence for each major bottleneck.

3. Generate plausible channel candidates.

4. Score and rank candidates against fixed criteria.

5. Select the top three channels.

6. Convert each recommendation into a repeatable operating system.

7. Define owners, metrics, dependencies, and success thresholds.

8. Check the final response against the schema.

The final report should expose concise rationales, evidence references, scoring, and explicit assumptions—not hidden internal reasoning.

### 6.3 Few-shot examples

Include at least one example in `PROMPT_ARCHITECTURE.md` showing:

* A miniature synthetic SaaS profile.

* Its key bottleneck.

* A sample ranked growth channel.

* A short explanation of the evidence behind the recommendation.

* A valid JSON response matching the same schema used in production.

The example must teach the model the required structure and reasoning standard without hardcoding the same answer for every company.

## 7. Output contract and JSON schema

The report should have a stable top-level structure with exactly three sections: `executive_summary`, `prioritized_growth_channels`, and `action_plan_30_days`.

### 7.1 Proposed schema

JSON

```
{
  "executive_summary": {
    "company_name": "string",
    "primary_bottleneck": "string",
    "key_findings": ["string"],
    "strategic_thesis": "string",
    "primary_30_day_objective": "string",
    "assumptions": ["string"]
  },
  "prioritized_growth_channels": [
    {
      "rank": 1,
      "channel": "string",
      "priority_score": 0,
      "rationale": "string",
      "supporting_evidence": ["string"],
      "system_to_build": "string",
      "leading_kpi": "string",
      "target": "string",
      "budget_usd": 0,
      "time_to_signal_days": 0,
      "risks": ["string"]
    }
  ],
  "action_plan_30_days": [
    {
      "week": 1,
      "theme": "string",
      "objective": "string",
      "actions": [
        {
          "task": "string",
          "owner": "string",
          "due_day": 1,
          "success_metric": "string",
          "deliverable": "string"
        }
      ]
    }
  ]
}
```

This is the conceptual contract. The implementation must define the same structure in Pydantic and use a JSON Schema derived from, or kept synchronized with, those models.

### 7.2 Schema enforcement rules

* Reject unknown properties using `extra="forbid"` in Pydantic.

* Require all mandatory fields.

* Enforce exactly three growth channels.

* Require ranks to be unique and ordered `1, 2, 3`.

* Require four weekly roadmap objects with weeks `1, 2, 3, 4`.

* Validate scores against a defined range, such as 0–100.

* Reject negative budgets and invalid day numbers.

* Restrict `due_day` to the 30-day implementation window.

* Limit string and array lengths to reasonable bounds.

* Use numeric types for numeric values, not numeric strings.

* Define whether missing metrics should be represented as assumptions or whether the report should fail validation.

Critical distinction: JSON parsing checks syntax; JSON Schema checks structure; business-rule validation checks whether the output makes sense. All three are necessary.

## 8. Strategy prioritization logic

The model must not select channels merely because they are popular. It should use a consistent scoring rubric.

| Criterion                | Weight |
| ------------------------ | ------ |
| Expected business impact | 35%    |
| Evidence of channel fit  | 25%    |
| Execution feasibility    | 20%    |
| Speed of learning        | 10%    |
| Cost efficiency          | 10%    |
| Total                    | 100%   |

Each criterion receives a score from 0 to 100. The weighted total is calculated as:

S=0.35I+0.25F+0.20E+0.10L+0.10CS = 0.35I + 0.25F + 0.20E + 0.10L + 0.10CS=0.35I+0.25F+0.20E+0.10L+0.10C

Where III = impact, FFF = fit, EEE = execution feasibility, LLL = learning speed, and CCC = cost efficiency.

The score is a prioritization aid, not a validated forecast of growth. The output should explain the evidence and uncertainties behind each ranking.

### 8.1 Example candidate channels

These are hypotheses for the synthetic company, not predetermined answers.

* Retention and lifecycle automation: Investigate whether high churn and below-100% net revenue retention justify prioritizing activation, onboarding, and customer-health workflows.

* Founder-led outbound: Test narrowly targeted prospecting for operations leaders instead of broad, expensive paid acquisition.

* Intent-driven organic acquisition: Improve conversion-focused content and lead capture around specific workflow automation problems.

The model may choose a different ranking if its rationale is consistent with the input data and constraints.

## 9. Thirty-day systems-first action plan

The report must produce four weekly phases. Each phase should build or improve a repeatable operating mechanism, not just list one-off promotional tasks.

| Phase               | Focus                         | Expected deliverable                                                      |
| ------------------- | ----------------------------- | ------------------------------------------------------------------------- |
| Week 1 · Days 1–7   | Instrumentation and diagnosis | Baseline metrics, funnel audit, churn/activation segmentation             |
| Week 2 · Days 8–14  | Build the initial systems     | Lifecycle triggers, outbound workflow, or content-to-lead tracking        |
| Week 3 · Days 15–21 | Run controlled experiments    | Experiment log, qualified-lead feedback, activation and retention signals |
| Week 4 · Days 22–30 | Review and operationalize     | Results report, documented playbooks, next-cycle priorities               |

The final plan must adapt these phases to the selected channels.

For every task, require:

* A specific action.

* One accountable owner or clearly defined role.

* A due day between 1 and 30.

* A measurable success metric.

* A concrete deliverable.

Targets must be distinguished from baselines and forecasts. If the input does not provide enough evidence to establish a credible numerical target, the report should specify a measurement or baseline-establishment task instead.

## 10. Technical architecture

### 10.1 Request lifecycle

Diagram options

![](data\:image/svg+xml;utf8,%3Csvg%20id%3D%22mermaid-_r_iq_%22%20width%3D%22612.3214111328125%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20class%3D%22flowchart%22%20height%3D%221240%22%20viewBox%3D%224%204%20612.3214111328125%201240%22%20role%3D%22graphics-document%20document%22%20aria-roledescription%3D%22flowchart-v2%22%3E%3Cstyle%3E%23mermaid-_r_iq_%7Bfont-family%3A%22-apple-system%22%2C%22BlinkMacSystemFont%22%2C%22Segoe%20UI%22%2C%22Roboto%22%2C%22Oxygen%22%2C%22Ubuntu%22%2C%22Cantarell%22%2C%22Helvetica%20Neue%22%2C%22Arial%22%2C%22sans-serif%22%3Bfont-size%3A14px%3Bfill%3Argb\(255%2C%20255%2C%20255\)%3B%7D%40keyframes%20edge-animation-frame%7Bfrom%7Bstroke-dashoffset%3A0%3B%7D%7D%40keyframes%20dash%7Bto%7Bstroke-dashoffset%3A0%3B%7D%7D%23mermaid-_r_iq_%20.edge-animation-slow%7Bstroke-dasharray%3A9%2C5!important%3Bstroke-dashoffset%3A900%3Banimation%3Adash%2050s%20linear%20infinite%3Bstroke-linecap%3Around%3B%7D%23mermaid-_r_iq_%20.edge-animation-fast%7Bstroke-dasharray%3A9%2C5!important%3Bstroke-dashoffset%3A900%3Banimation%3Adash%2020s%20linear%20infinite%3Bstroke-linecap%3Around%3B%7D%23mermaid-_r_iq_%20.error-icon%7Bfill%3Argb\(33%2C%2033%2C%2033\)%3B%7D%23mermaid-_r_iq_%20.error-text%7Bfill%3Argb\(255%2C%20255%2C%20255\)%3Bstroke%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20.edge-thickness-normal%7Bstroke-width%3A1px%3B%7D%23mermaid-_r_iq_%20.edge-thickness-thick%7Bstroke-width%3A3.5px%3B%7D%23mermaid-_r_iq_%20.edge-pattern-solid%7Bstroke-dasharray%3A0%3B%7D%23mermaid-_r_iq_%20.edge-thickness-invisible%7Bstroke-width%3A0%3Bfill%3Anone%3B%7D%23mermaid-_r_iq_%20.edge-pattern-dashed%7Bstroke-dasharray%3A3%3B%7D%23mermaid-_r_iq_%20.edge-pattern-dotted%7Bstroke-dasharray%3A2%3B%7D%23mermaid-_r_iq_%20.marker%7Bfill%3Argb\(205%2C%20205%2C%20205\)%3Bstroke%3Argb\(205%2C%20205%2C%20205\)%3B%7D%23mermaid-_r_iq_%20.marker.cross%7Bstroke%3Argb\(205%2C%20205%2C%20205\)%3B%7D%23mermaid-_r_iq_%20svg%7Bfont-family%3A%22-apple-system%22%2C%22BlinkMacSystemFont%22%2C%22Segoe%20UI%22%2C%22Roboto%22%2C%22Oxygen%22%2C%22Ubuntu%22%2C%22Cantarell%22%2C%22Helvetica%20Neue%22%2C%22Arial%22%2C%22sans-serif%22%3Bfont-size%3A14px%3B%7D%23mermaid-_r_iq_%20p%7Bmargin%3A0%3B%7D%23mermaid-_r_iq_%20.label%7Bfont-family%3A%22-apple-system%22%2C%22BlinkMacSystemFont%22%2C%22Segoe%20UI%22%2C%22Roboto%22%2C%22Oxygen%22%2C%22Ubuntu%22%2C%22Cantarell%22%2C%22Helvetica%20Neue%22%2C%22Arial%22%2C%22sans-serif%22%3Bcolor%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20.cluster-label%20text%7Bfill%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20.cluster-label%20span%7Bcolor%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20.cluster-label%20span%20p%7Bbackground-color%3Atransparent%3B%7D%23mermaid-_r_iq_%20.label%20text%2C%23mermaid-_r_iq_%20span%7Bfill%3Argb\(255%2C%20255%2C%20255\)%3Bcolor%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20.node%20rect%2C%23mermaid-_r_iq_%20.node%20circle%2C%23mermaid-_r_iq_%20.node%20ellipse%2C%23mermaid-_r_iq_%20.node%20polygon%2C%23mermaid-_r_iq_%20.node%20path%7Bfill%3Argb\(9%2C%2023%2C%2044\)%3Bstroke%3Argb\(31%2C%2078%2C%20148\)%3Bstroke-width%3A1px%3B%7D%23mermaid-_r_iq_%20.rough-node%20.label%20text%2C%23mermaid-_r_iq_%20.node%20.label%20text%2C%23mermaid-_r_iq_%20.image-shape%20.label%2C%23mermaid-_r_iq_%20.icon-shape%20.label%7Btext-anchor%3Amiddle%3B%7D%23mermaid-_r_iq_%20.node%20.katex%20path%7Bfill%3A%23000%3Bstroke%3A%23000%3Bstroke-width%3A1px%3B%7D%23mermaid-_r_iq_%20.rough-node%20.label%2C%23mermaid-_r_iq_%20.node%20.label%2C%23mermaid-_r_iq_%20.image-shape%20.label%2C%23mermaid-_r_iq_%20.icon-shape%20.label%7Btext-align%3Acenter%3B%7D%23mermaid-_r_iq_%20.node.clickable%7Bcursor%3Apointer%3B%7D%23mermaid-_r_iq_%20.root%20.anchor%20path%7Bfill%3Argb\(205%2C%20205%2C%20205\)!important%3Bstroke-width%3A0%3Bstroke%3Argb\(205%2C%20205%2C%20205\)%3B%7D%23mermaid-_r_iq_%20.arrowheadPath%7Bfill%3Argb\(205%2C%20205%2C%20205\)%3B%7D%23mermaid-_r_iq_%20.edgePath%20.path%7Bstroke%3Argb\(205%2C%20205%2C%20205\)%3Bstroke-width%3A2.0px%3B%7D%23mermaid-_r_iq_%20.flowchart-link%7Bstroke%3Argb\(205%2C%20205%2C%20205\)%3Bfill%3Anone%3B%7D%23mermaid-_r_iq_%20.edgeLabel%7Bbackground-color%3Argb\(0%2C%200%2C%200\)%3Btext-align%3Acenter%3B%7D%23mermaid-_r_iq_%20.edgeLabel%20p%7Bbackground-color%3Argb\(0%2C%200%2C%200\)%3B%7D%23mermaid-_r_iq_%20.edgeLabel%20rect%7Bopacity%3A0.5%3Bbackground-color%3Argb\(0%2C%200%2C%200\)%3Bfill%3Argb\(0%2C%200%2C%200\)%3B%7D%23mermaid-_r_iq_%20.labelBkg%7Bbackground-color%3Argba\(0%2C%200%2C%200%2C%200.5\)%3B%7D%23mermaid-_r_iq_%20.cluster%20rect%7Bfill%3Argb\(33%2C%2033%2C%2033\)%3Bstroke%3Argba\(255%2C%20255%2C%20255%2C%200.05\)%3Bstroke-width%3A1px%3B%7D%23mermaid-_r_iq_%20.cluster%20text%7Bfill%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20.cluster%20span%7Bcolor%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20div.mermaidTooltip%7Bposition%3Aabsolute%3Btext-align%3Acenter%3Bmax-width%3A200px%3Bpadding%3A2px%3Bfont-family%3A%22-apple-system%22%2C%22BlinkMacSystemFont%22%2C%22Segoe%20UI%22%2C%22Roboto%22%2C%22Oxygen%22%2C%22Ubuntu%22%2C%22Cantarell%22%2C%22Helvetica%20Neue%22%2C%22Arial%22%2C%22sans-serif%22%3Bfont-size%3A12px%3Bbackground%3Argb\(33%2C%2033%2C%2033\)%3Bborder%3A1px%20solid%20rgba\(255%2C%20255%2C%20255%2C%200.05\)%3Bborder-radius%3A2px%3Bpointer-events%3Anone%3Bz-index%3A100%3B%7D%23mermaid-_r_iq_%20.flowchartTitleText%7Btext-anchor%3Amiddle%3Bfont-size%3A18px%3Bfill%3Argb\(255%2C%20255%2C%20255\)%3B%7D%23mermaid-_r_iq_%20rect.text%7Bfill%3Anone%3Bstroke-width%3A0%3B%7D%23mermaid-_r_iq_%20.icon-shape%2C%23mermaid-_r_iq_%20.image-shape%7Bbackground-color%3Argb\(0%2C%200%2C%200\)%3Btext-align%3Acenter%3B%7D%23mermaid-_r_iq_%20.icon-shape%20p%2C%23mermaid-_r_iq_%20.image-shape%20p%7Bbackground-color%3Argb\(0%2C%200%2C%200\)%3Bpadding%3A2px%3B%7D%23mermaid-_r_iq_%20.icon-shape%20rect%2C%23mermaid-_r_iq_%20.image-shape%20rect%7Bopacity%3A0.5%3Bbackground-color%3Argb\(0%2C%200%2C%200\)%3Bfill%3Argb\(0%2C%200%2C%200\)%3B%7D%23mermaid-_r_iq_%20.label-icon%7Bdisplay%3Ainline-block%3Bheight%3A1em%3Boverflow%3Avisible%3Bvertical-align%3A-0.125em%3B%7D%23mermaid-_r_iq_%20.node%20.label-icon%20path%7Bfill%3AcurrentColor%3Bstroke%3Arevert%3Bstroke-width%3Arevert%3B%7D%23mermaid-_r_iq_%20.node%20text%7Bfont-size%3A16px%3Bfont-weight%3A600%3Bletter-spacing%3A-0.32px%3Bfill%3A%2399ceff%3B%7D%23mermaid-_r_iq_%20.edgeLabels%20text%7Bfont-size%3A13px%3Bfont-weight%3A600%3Bletter-spacing%3A-0.08px%3Bfill%3A%2399ceff%3B%7D%23mermaid-_r_iq_%20.node%20tspan%5Bfont-weight%3D%22normal%22%5D%2C%23mermaid-_r_iq_%20.edgeLabels%20tspan%5Bfont-weight%3D%22normal%22%5D%7Bfont-weight%3A600%3B%7D%23mermaid-_r_iq_%20.edgeLabel%20.label%20rect%7Bopacity%3A1%3Brx%3A13px%3Bry%3A13px%3Bfill%3A%23000e1a%3Bstroke%3Argb\(26%2C%2062%2C%2095\)%3Bstroke-width%3A1px%3B%7D%23mermaid-_r_iq_%20.node%20rect%2C%23mermaid-_r_iq_%20.node%20circle%2C%23mermaid-_r_iq_%20.node%20ellipse%2C%23mermaid-_r_iq_%20.node%20polygon%2C%23mermaid-_r_iq_%20.node%20path%7Bfill%3Argb\(0%2C%2040%2C%2077\)%3Bstroke%3Argba\(255%2C%20255%2C%20255%2C%200.1\)%3Bstroke-width%3A1px%3B%7D%23mermaid-_r_iq_%20.node%20rect%7Brx%3A16px%3Bry%3A16px%3B%7D%23mermaid-_r_iq_%20.node.mermaid-decision%20.label-container%7Bfill%3A%23000e1a%3Bstroke%3Argb\(26%2C%2062%2C%2095\)%3Bstroke-dasharray%3A2%202%3B%7D%23mermaid-_r_iq_%20.edgePaths%20.flowchart-link%7Bstroke%3Argb\(26%2C%2062%2C%2095\)%3Bstroke-width%3A1px%3Bstroke-linecap%3Around%3Bstroke-linejoin%3Around%3B%7D%23mermaid-_r_iq_%20.marker%7Bfill%3Argb\(26%2C%2062%2C%2095\)%3Bstroke%3Argb\(26%2C%2062%2C%2095\)%3B%7D%23mermaid-_r_iq_%20.node%7Bcolor-scheme%3Adark%3B%7D%23mermaid-_r_iq_%20%3Aroot%7B--mermaid-font-family%3A%22-apple-system%22%2C%22BlinkMacSystemFont%22%2C%22Segoe%20UI%22%2C%22Roboto%22%2C%22Oxygen%22%2C%22Ubuntu%22%2C%22Cantarell%22%2C%22Helvetica%20Neue%22%2C%22Arial%22%2C%22sans-serif%22%3B%7D%3C%2Fstyle%3E%3Cg%3E%3Cmarker%20id%3D%22mermaid-_r_iq__flowchart-v2-pointEnd%22%20class%3D%22marker%20flowchart-v2%22%20viewBox%3D%22-5%20-5%2010%2010%22%20refX%3D%220%22%20refY%3D%220%22%20markerUnits%3D%22userSpaceOnUse%22%20markerWidth%3D%2210%22%20markerHeight%3D%2210%22%20orient%3D%22auto%22%3E%3Cpath%20d%3D%22M%200%200%20L%204%200%20M%200.8180194846605362%20-3.181980515339464%20L%204%200%20L%200.8180194846605362%203.181980515339464%22%20class%3D%22arrowMarkerPath%22%20style%3D%22stroke-width%3A%201%3B%20stroke-dasharray%3A%20none%3B%20fill%3A%20none%3B%20stroke-linecap%3A%20round%3B%20stroke-linejoin%3A%20round%3B%22%3E%3C%2Fpath%3E%3C%2Fmarker%3E%3Cmarker%20id%3D%22mermaid-_r_iq__flowchart-v2-pointStart%22%20class%3D%22marker%20flowchart-v2%22%20viewBox%3D%22-5%20-5%2010%2010%22%20refX%3D%220%22%20refY%3D%220%22%20markerUnits%3D%22userSpaceOnUse%22%20markerWidth%3D%2210%22%20markerHeight%3D%2210%22%20orient%3D%22auto%22%3E%3Cpath%20d%3D%22M%200%200%20L%20-4%200%20M%20-0.8180194846605362%20-3.181980515339464%20L%20-4%200%20L%20-0.8180194846605362%203.181980515339464%22%20class%3D%22arrowMarkerPath%22%20style%3D%22stroke-width%3A%201%3B%20stroke-dasharray%3A%20none%3B%20fill%3A%20none%3B%20stroke-linecap%3A%20round%3B%20stroke-linejoin%3A%20round%3B%22%3E%3C%2Fpath%3E%3C%2Fmarker%3E%3Cmarker%20id%3D%22mermaid-_r_iq__flowchart-v2-circleEnd%22%20class%3D%22marker%20flowchart-v2%22%20viewBox%3D%220%200%2010%2010%22%20refX%3D%2211%22%20refY%3D%225%22%20markerUnits%3D%22userSpaceOnUse%22%20markerWidth%3D%2211%22%20markerHeight%3D%2211%22%20orient%3D%22auto%22%3E%3Ccircle%20cx%3D%225%22%20cy%3D%225%22%20r%3D%225%22%20class%3D%22arrowMarkerPath%22%20style%3D%22stroke-width%3A%201%3B%20stroke-dasharray%3A%201%2C%200%3B%22%3E%3C%2Fcircle%3E%3C%2Fmarker%3E%3Cmarker%20id%3D%22mermaid-_r_iq__flowchart-v2-circleStart%22%20class%3D%22marker%20flowchart-v2%22%20viewBox%3D%220%200%2010%2010%22%20refX%3D%22-1%22%20refY%3D%225%22%20markerUnits%3D%22userSpaceOnUse%22%20markerWidth%3D%2211%22%20markerHeight%3D%2211%22%20orient%3D%22auto%22%3E%3Ccircle%20cx%3D%225%22%20cy%3D%225%22%20r%3D%225%22%20class%3D%22arrowMarkerPath%22%20style%3D%22stroke-width%3A%201%3B%20stroke-dasharray%3A%201%2C%200%3B%22%3E%3C%2Fcircle%3E%3C%2Fmarker%3E%3Cmarker%20id%3D%22mermaid-_r_iq__flowchart-v2-crossEnd%22%20class%3D%22marker%20cross%20flowchart-v2%22%20viewBox%3D%220%200%2011%2011%22%20refX%3D%2212%22%20refY%3D%225.2%22%20markerUnits%3D%22userSpaceOnUse%22%20markerWidth%3D%2211%22%20markerHeight%3D%2211%22%20orient%3D%22auto%22%3E%3Cpath%20d%3D%22M%201%2C1%20l%209%2C9%20M%2010%2C1%20l%20-9%2C9%22%20class%3D%22arrowMarkerPath%22%20style%3D%22stroke-width%3A%202%3B%20stroke-dasharray%3A%201%2C%200%3B%22%3E%3C%2Fpath%3E%3C%2Fmarker%3E%3Cmarker%20id%3D%22mermaid-_r_iq__flowchart-v2-crossStart%22%20class%3D%22marker%20cross%20flowchart-v2%22%20viewBox%3D%220%200%2011%2011%22%20refX%3D%22-1%22%20refY%3D%225.2%22%20markerUnits%3D%22userSpaceOnUse%22%20markerWidth%3D%2211%22%20markerHeight%3D%2211%22%20orient%3D%22auto%22%3E%3Cpath%20d%3D%22M%201%2C1%20l%209%2C9%20M%2010%2C1%20l%20-9%2C9%22%20class%3D%22arrowMarkerPath%22%20style%3D%22stroke-width%3A%202%3B%20stroke-dasharray%3A%201%2C%200%3B%22%3E%3C%2Fpath%3E%3C%2Fmarker%3E%3C%2Fg%3E%3Cg%20class%3D%22subgraphs%22%3E%3C%2Fg%3E%3Cg%20class%3D%22nodes%22%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-A-0%22%20transform%3D%22translate\(346.9817937215169%2C%2042\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-112.14375305175781%22%20y%3D%22-30%22%20width%3D%22224.28750610351562%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3ELoad%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20company%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20JSON%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-B-1%22%20transform%3D%22translate\(346.9817937215169%2C%20142\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-85.77187728881836%22%20y%3D%22-30%22%20width%3D%22171.54375457763672%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EValidate%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20input%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-C-3%22%20transform%3D%22translate\(112.88777160644531%2C%20308\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-100.88777160644531%22%20y%3D%22-30%22%20width%3D%22201.77554321289062%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EReturn%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20input%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20error%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-D-5%22%20transform%3D%22translate\(375.5724182128906%2C%20308\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-121.796875%22%20y%3D%22-30%22%20width%3D%22243.59375%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EBuild%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20layered%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20messages%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-E-7%22%20transform%3D%22translate\(375.5724182128906%2C%20408\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-83.75%22%20y%3D%22-30%22%20width%3D%22167.5%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3ECall%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20Groq%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20API%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-F-9%22%20transform%3D%22translate\(375.5724182128906%2C%20508\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-122.25%22%20y%3D%22-30%22%20width%3D%22244.5%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EExtract%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20model%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20response%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-G-11%22%20transform%3D%22translate\(375.5724182128906%2C%20608\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-79.3687515258789%22%20y%3D%22-30%22%20width%3D%22158.7375030517578%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EParse%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20JSON%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-H-13%22%20transform%3D%22translate\(243.46825154622394%2C%201106\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-86.515625%22%20y%3D%22-30%22%20width%3D%22173.03125%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3ERecord%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20failure%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-I-15%22%20transform%3D%22translate\(402.0286687215169%2C%20774\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-129.58438110351562%22%20y%3D%22-30%22%20width%3D%22259.16876220703125%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EValidate%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20Pydantic%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20schema%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-J-19%22%20transform%3D%22translate\(445.2234624226888%2C%20940\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-119.45000457763672%22%20y%3D%22-30%22%20width%3D%22238.90000915527344%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EValidate%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20business%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20rules%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-K-23%22%20transform%3D%22translate\(485.04012807210285%2C%201106\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-115.0562515258789%22%20y%3D%22-30%22%20width%3D%22230.1125030517578%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EWrite%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20validated%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20report%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22node%20default%22%20id%3D%22flowchart-L-25%22%20transform%3D%22translate\(485.04012807210285%2C%201206\)%22%3E%3Crect%20class%3D%22basic%20label-container%22%20style%3D%22%22%20x%3D%22-123.28125762939453%22%20y%3D%22-30%22%20width%3D%22246.56251525878906%22%20height%3D%2260%22%3E%3C%2Frect%3E%3Cg%20class%3D%22label%22%20style%3D%22%22%20transform%3D%22translate\(0%2C%20-9.40000057220459\)%22%3E%3Crect%3E%3C%2Frect%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3ELog%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20execution%3C%2Ftspan%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3E%20metadata%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edges%20edgePaths%22%3E%3Cpath%20d%3D%22M346.9817937215169%2C72L346.9817937215169%2C100%22%20id%3D%22L_A_B_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_A_B_0%22%20data-points%3D%22W3sieCI6MzQ2Ljk4MTc5MzcyMTUxNjksInkiOjcyfSx7IngiOjM0Ni45ODE3OTM3MjE1MTY5LCJ5IjoxMDR9XQ%3D%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M318.3911692301432%2C172L318.3911692301432%2C185.21704397470535Q318.3911692301432%2C187%20317.3053827925163%2C188.4142135623731L317.3053827925163%2C188.4142135623731Q316.2195963548894%2C189.82842712474618%20314.8053827925163%2C190.91421356237308L314.8053827925163%2C190.9142135623731Q313.3911692301432%2C192%20311.60821320484854%2C192L119.67072763173996%2C192Q117.88777160644531%2C192%20116.47355804407222%2C193.0857864376269L116.47355804407222%2C193.0857864376269Q115.05934448169913%2C194.17157287525382%20113.97355804407222%2C195.5857864376269L113.97355804407222%2C195.5857864376269Q112.88777160644531%2C197%20112.88777160644531%2C198.78295602529465L112.88777160644531%2C266%22%20id%3D%22L_B_C_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_B_C_0%22%20data-points%3D%22W3sieCI6MzE4LjM5MTE2OTIzMDE0MzIsInkiOjE3Mn0seyJ4IjozMTguMzkxMTY5MjMwMTQzMiwieSI6MTkyfSx7IngiOjExMi44ODc3NzE2MDY0NDUzMSwieSI6MTkyfSx7IngiOjExMi44ODc3NzE2MDY0NDUzMSwieSI6MjcwfV0%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M375.5724182128906%2C172L375.5724182128906%2C266%22%20id%3D%22L_B_D_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_B_D_0%22%20data-points%3D%22W3sieCI6Mzc1LjU3MjQxODIxMjg5MDYsInkiOjE3Mn0seyJ4IjozNzUuNTcyNDE4MjEyODkwNiwieSI6MjcwfV0%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M375.5724182128906%2C338L375.5724182128906%2C366%22%20id%3D%22L_D_E_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_D_E_0%22%20data-points%3D%22W3sieCI6Mzc1LjU3MjQxODIxMjg5MDYsInkiOjMzOH0seyJ4IjozNzUuNTcyNDE4MjEyODkwNiwieSI6MzcwfV0%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M375.5724182128906%2C438L375.5724182128906%2C466%22%20id%3D%22L_E_F_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_E_F_0%22%20data-points%3D%22W3sieCI6Mzc1LjU3MjQxODIxMjg5MDYsInkiOjQzOH0seyJ4IjozNzUuNTcyNDE4MjEyODkwNiwieSI6NDcwfV0%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M375.5724182128906%2C538L375.5724182128906%2C566%22%20id%3D%22L_F_G_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_F_G_0%22%20data-points%3D%22W3sieCI6Mzc1LjU3MjQxODIxMjg5MDYsInkiOjUzOH0seyJ4IjozNzUuNTcyNDE4MjEyODkwNiwieSI6NTcwfV0%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M349.1161677042643%2C638L349.1161677042643%2C651.2170439747053Q349.1161677042643%2C653%20348.0303812666374%2C654.4142135623731L348.0303812666374%2C654.4142135623731Q346.9445948290105%2C655.8284271247462%20345.5303812666374%2C656.9142135623731L345.5303812666374%2C656.9142135623731Q344.1161677042643%2C658%20342.33321167896963%2C658L196.7512075715186%2C658Q194.96825154622394%2C658%20193.55403798385083%2C659.0857864376269L193.55403798385083%2C659.0857864376269Q192.13982442147775%2C660.1715728752538%20191.05403798385086%2C661.5857864376269L191.05403798385083%2C661.5857864376269Q189.96825154622394%2C663%20189.96825154622394%2C664.7829560252947L189.96825154622394%2C691L189.96825154622394%2C774L189.96825154622394%2C940L189.96825154622394%2C1023L189.96825154622394%2C1049.2170439747053Q189.96825154622394%2C1051%20191.05403798385083%2C1052.414213562373L191.05403798385086%2C1052.414213562373Q192.13982442147775%2C1053.8284271247462%20193.55403798385083%2C1054.914213562373L194.87220182814954%2C1055.9262562006206Q194.96825154622394%2C1056%20195.08934529622394%2C1056L195.08934529622394%2C1056Q195.21043904622394%2C1056%20195.30648876429834%2C1056.0737437993794L196.62465260859705%2C1057.085786437627Q198.03886617097012%2C1058.1715728752538%20199.12465260859702%2C1059.585786437627L199.12465260859705%2C1059.585786437627Q200.21043904622394%2C1061%20200.21043904622394%2C1062.7829560252947L200.21043904622394%2C1066%22%20id%3D%22L_G_H_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_G_H_0%22%20data-points%3D%22W3sieCI6MzQ5LjExNjE2NzcwNDI2NDMsInkiOjYzOH0seyJ4IjozNDkuMTE2MTY3NzA0MjY0MywieSI6NjU4fSx7IngiOjE4OS45NjgyNTE1NDYyMjM5NCwieSI6NjU4fSx7IngiOjE4OS45NjgyNTE1NDYyMjM5NCwieSI6NjkxfSx7IngiOjE4OS45NjgyNTE1NDYyMjM5NCwieSI6Nzc0fSx7IngiOjE4OS45NjgyNTE1NDYyMjM5NCwieSI6OTQwfSx7IngiOjE4OS45NjgyNTE1NDYyMjM5NCwieSI6MTAyM30seyJ4IjoxODkuOTY4MjUxNTQ2MjIzOTQsInkiOjEwNTZ9LHsieCI6MjAwLjIxMDQzOTA0NjIyMzk0LCJ5IjoxMDU2fSx7IngiOjIwMC4yMTA0MzkwNDYyMjM5NCwieSI6MTA3MH1d%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M402.0286687215169%2C638L402.0286687215169%2C732%22%20id%3D%22L_G_I_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_G_I_0%22%20data-points%3D%22W3sieCI6NDAyLjAyODY2ODcyMTUxNjksInkiOjYzOH0seyJ4Ijo0MDIuMDI4NjY4NzIxNTE2OSwieSI6NzM2fV0%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M358.833875020345%2C804L358.83387502034503%2C816.9289321881346Q358.83387502034503%2C824%20351.76280720847956%2C824L250.2512075715186%2C824Q248.46825154622394%2C824%20247.05403798385083%2C825.0857864376269L247.05403798385083%2C825.0857864376269Q245.63982442147775%2C826.1715728752538%20244.55403798385086%2C827.5857864376269L244.55403798385083%2C827.5857864376269Q243.46825154622394%2C829%20243.46825154622394%2C830.7829560252947L243.46825154622394%2C857L243.46825154622394%2C1023L243.46825154622394%2C1064%22%20id%3D%22L_I_H_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_I_H_0%22%20data-points%3D%22W3sieCI6MzU4LjgzMzg3NTAyMDM0NSwieSI6ODA0fSx7IngiOjM1OC44MzM4NzUwMjAzNDUwMywieSI6ODI0fSx7IngiOjI0My40NjgyNTE1NDYyMjM5NCwieSI6ODI0fSx7IngiOjI0My40NjgyNTE1NDYyMjM5NCwieSI6ODU3fSx7IngiOjI0My40NjgyNTE1NDYyMjM5NCwieSI6MTAyM30seyJ4IjoyNDMuNDY4MjUxNTQ2MjIzOTQsInkiOjEwNjh9XQ%3D%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M445.22346242268884%2C804L445.2234624226888%2C898%22%20id%3D%22L_I_J_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_I_J_0%22%20data-points%3D%22W3sieCI6NDQ1LjIyMzQ2MjQyMjY4ODg0LCJ5Ijo4MDR9LHsieCI6NDQ1LjIyMzQ2MjQyMjY4ODgsInkiOjkwMn1d%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M405.4067967732748%2C970L405.4067967732747%2C989.9291648864746Q405.4067967732747%2C990%20405.33596165974933%2C990L405.33596165974933%2C990Q405.26512654622394%2C990%20405.26512654622394%2C990.0708351135254L405.26512654622394%2C1049.2170439747053Q405.26512654622394%2C1051%20404.17934010859705%2C1052.414213562373L404.17934010859705%2C1052.414213562373Q403.09355367097015%2C1053.8284271247462%20401.67934010859705%2C1054.914213562373L401.67934010859705%2C1054.914213562373Q400.26512654622394%2C1056%20398.4821705209293%2C1056L293.5090200715186%2C1056Q291.72606404622394%2C1056%20290.31185048385083%2C1057.085786437627L290.31185048385083%2C1057.085786437627Q288.8976369214777%2C1058.1715728752538%20287.81185048385083%2C1059.585786437627L287.81185048385083%2C1059.585786437627Q286.72606404622394%2C1061%20286.72606404622394%2C1062.7829560252947L286.72606404622394%2C1066%22%20id%3D%22L_J_H_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_J_H_0%22%20data-points%3D%22W3sieCI6NDA1LjQwNjc5Njc3MzI3NDgsInkiOjk3MH0seyJ4Ijo0MDUuNDA2Nzk2NzczMjc0NywieSI6OTkwfSx7IngiOjQwNS4yNjUxMjY1NDYyMjM5NCwieSI6OTkwfSx7IngiOjQwNS4yNjUxMjY1NDYyMjM5NCwieSI6MTA1Nn0seyJ4IjoyODYuNzI2MDY0MDQ2MjIzOTQsInkiOjEwNTZ9LHsieCI6Mjg2LjcyNjA2NDA0NjIyMzk0LCJ5IjoxMDcwfV0%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M485.0401280721028%2C970L485.04012807210285%2C1064%22%20id%3D%22L_J_K_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_J_K_0%22%20data-points%3D%22W3sieCI6NDg1LjA0MDEyODA3MjEwMjgsInkiOjk3MH0seyJ4Ijo0ODUuMDQwMTI4MDcyMTAyODUsInkiOjEwNjh9XQ%3D%3D%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3Cpath%20d%3D%22M485.04012807210285%2C1136L485.04012807210285%2C1164%22%20id%3D%22L_K_L_0%22%20class%3D%22edge-thickness-normal%20edge-pattern-solid%20edge-thickness-normal%20edge-pattern-solid%20flowchart-link%22%20style%3D%22%3B%22%20data-edge%3D%22true%22%20data-et%3D%22edge%22%20data-id%3D%22L_K_L_0%22%20data-points%3D%22W3sieCI6NDg1LjA0MDEyODA3MjEwMjg1LCJ5IjoxMTM2fSx7IngiOjQ4NS4wNDAxMjgwNzIxMDI4NSwieSI6MTE2OH1d%22%20marker-end%3D%22url\(%23mermaid-_r_iq__flowchart-v2-pointEnd\)%22%3E%3C%2Fpath%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabels%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3C%2Fg%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3C%2Fg%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3C%2Fg%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3C%2Fg%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22stroke%3A%20none%22%3E%3C%2Frect%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_A_B_0%22%20transform%3D%22translate\(0%2C%200\)%22%3E%3Ctext%20y%3D%22-10.1%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(112.77527236938477%2C%20225\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_B_C_0%22%20transform%3D%22translate\(-20.387500762939453%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2264.7750015258789%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EInvalid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(375.4099178314209%2C%20225\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_B_D_0%22%20transform%3D%22translate\(-15.337499618530273%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2254.67500114440918%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EValid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_D_E_0%22%20transform%3D%22translate\(0%2C%200\)%22%3E%3Ctext%20y%3D%22-10.1%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_E_F_0%22%20transform%3D%22translate\(0%2C%200\)%22%3E%3Ctext%20y%3D%22-10.1%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_F_G_0%22%20transform%3D%22translate\(0%2C%200\)%22%3E%3Ctext%20y%3D%22-10.1%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(189.8557523091634%2C%20857\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_G_H_0%22%20transform%3D%22translate\(-20.387500762939453%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2264.7750015258789%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EInvalid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(401.8661683400472%2C%20691\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_G_I_0%22%20transform%3D%22translate\(-15.337499618530273%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2254.67500114440918%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EValid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(243.3557523091634%2C%20940\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_I_H_0%22%20transform%3D%22translate\(-20.387500762939453%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2264.7750015258789%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EInvalid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(445.06096204121906%2C%20857\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_I_J_0%22%20transform%3D%22translate\(-15.337499618530273%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2254.67500114440918%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EValid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(405.1526273091634%2C%201023\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_J_H_0%22%20transform%3D%22translate\(-20.387500762939453%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2264.7750015258789%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EInvalid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%20transform%3D%22translate\(484.8776276906331%2C%201023\)%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_J_K_0%22%20transform%3D%22translate\(-15.337499618530273%2C-8.199999809265137\)%22%3E%3Cg%3E%3Crect%20class%3D%22background%22%20style%3D%22%22%20x%3D%22-12%22%20y%3D%22-4.800000071525574%22%20width%3D%2254.67500114440918%22%20height%3D%2226%22%3E%3C%2Frect%3E%3Ctext%20y%3D%22-10.1%22%20style%3D%22%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3Ctspan%20font-style%3D%22normal%22%20class%3D%22text-inner-tspan%22%20font-weight%3D%22normal%22%3EValid%3C%2Ftspan%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3Cg%20class%3D%22edgeLabel%22%3E%3Cg%20class%3D%22label%22%20data-id%3D%22L_K_L_0%22%20transform%3D%22translate\(0%2C%200\)%22%3E%3Ctext%20y%3D%22-10.1%22%3E%3Ctspan%20class%3D%22text-outer-tspan%22%20x%3D%220%22%20y%3D%22-0.1em%22%20dy%3D%221.1em%22%3E%3C%2Ftspan%3E%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E)

A failure at any validation stage must not produce a successful report file. If corrective retries are implemented, the retry must be bounded and the final result must pass the complete validation pipeline.

### 10.2 Suggested repository structure

```
llm-brain/
├── README.md
├── PROMPT_ARCHITECTURE.md
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   └── saas_company.json
├── prompts/
│   ├── system.md
│   ├── strategy_procedure.md
│   └── few_shot_examples.json
├── schemas/
│   └── report_schema.py
├── src/
│   ├── main.py
│   ├── config.py
│   ├── prompt_builder.py
│   ├── groq_client.py
│   ├── validator.py
│   └── logger.py
├── tests/
│   ├── test_schema.py
│   ├── test_business_rules.py
│   ├── test_prompt_builder.py
│   └── test_integration.py
├── outputs/
│   └── sample_report.json
└── logs/
    └── runs.jsonl
```

Keep `outputs/` and `logs/` out of Git if they may contain sensitive information. The synthetic sample report can be committed separately as a deliberate demonstration artifact.

### 10.3 Core module responsibilities

| Module              | Responsibility                                                   |
| ------------------- | ---------------------------------------------------------------- |
| `config.py`         | Load API credentials, model name, timeout, and token limits      |
| `prompt_builder.py` | Assemble versioned prompts and inject validated business context |
| `groq_client.py`    | Call the model and handle API-level errors                       |
| `report_schema.py`  | Define Pydantic models and generate the JSON Schema              |
| `validator.py`      | Parse output and enforce structural and semantic rules           |
| `logger.py`         | Persist JSONL run records and safe execution metadata            |
| `main.py`           | Coordinate the pipeline and write the final report               |

## 11. API and environment specification

### Environment variables

`.env.example`

Bash

```
GROQ_API_KEY=replace_with_your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
REQUEST_TIMEOUT_SECONDS=60
MAX_RETRIES=1
MAX_OUTPUT_TOKENS=5000
PROMPT_VERSION=1.0.0
```

The values are initial configuration defaults, not guarantees about current Groq model availability, token limits, or account quotas.

### Expected execution interface

Bash

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main \
  --input data/saas_company.json \
  --output outputs/sample_report.json
```

The application should exit with code `0` on success and a nonzero exit code on API, parsing, or validation failure. Error messages should identify the failing stage without exposing credentials.

## 12. Logging and observability

Each execution should generate one structured log record with the following fields:

| Field               | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `run_id`            | Unique execution identifier                           |
| `timestamp_utc`     | Execution start or completion timestamp               |
| `prompt_version`    | Version of the prompt architecture                    |
| `model`             | Model requested                                       |
| `input_hash`        | Optional hash of canonicalized input data             |
| `status`            | `success` or `failure`                                |
| `latency_ms`        | End-to-end model and processing latency               |
| `usage`             | Prompt and completion tokens when returned by the API |
| `validation_errors` | Empty array on success; error details on failure      |
| `output_path`       | Path to the validated report when successful          |
| `error_type`        | Sanitized error category when failed                  |

Log the complete prompt and raw response only when needed for reproducibility, with an explicit policy for retention and redaction. Never record the API key. For this synthetic demonstration, logging full inputs and outputs is acceptable; production use should apply data minimization.

## 13. Testing and acceptance plan

The submission is complete only when the following tests have been executed.

T01 — Valid report parsing

A correctly formatted JSON report parses successfully.

T02 — Missing required field

A report missing executive summary fields is rejected.

T03 — Unexpected field

An additional root or nested key is rejected.

T04 — Incorrect channel count

Reports containing two or four channels are rejected.

T05 — Incorrect roadmap duration

Missing weeks, duplicate weeks, or invalid day numbers are rejected.

T06 — Type mismatch

A string in a numeric field is rejected or coerced only if explicitly permitted by the contract.

T07 — API failure

A timeout or rate limit results in a controlled failure and bounded retry.

T08 — End-to-end run

A live Groq call produces a saved report that passes all validators.

T09 — Logging

Success and failure paths produce structured run logs.

T10 — Prompt consistency

The prompt's output requirements match the implemented schema.

### Test execution

Bash

```
pytest -q
python -m src.main \
  --input data/saas_company.json \
  --output outputs/sample_report.json
```

Use mocks for deterministic unit tests and a separate live API integration test for actual model behavior. Do not mark the integration test as passed unless it has been run against the configured API.

### Definition of done

* Prompt architecture document is complete.

* Synthetic business context is included.

* System prompt, strategy procedure, and few-shot example are implemented.

* Pydantic schema and JSON Schema agree.

* Exactly three growth channels are validated.

* Four roadmap phases cover the full 30-day period.

* Extra fields and malformed responses are rejected.

* Logging works for both success and failure.

* Automated tests have been executed.

* A real LLM-generated JSON report is saved as a sample.

* README documents setup, configuration, execution, and limitations.

## 14. Deliverables

The assignment requires three core artifacts, with supporting project files recommended for reproducibility.

1. `PROMPT_ARCHITECTURE.md`

Persona and constraints, context-injection strategy, reasoning procedure, few-shot example, schema contract, prioritization rubric, and failure-handling rules.

2. Python implementation

Prompt builder, Groq API client, input and output validation, logging, configuration, and automated tests.

3. `outputs/sample_report.json`

The exact final JSON generated by a real successful LLM run, saved only after validation. It must not be a fabricated example presented as model output.

Recommended additions: `README.md`, `.env.example`, `requirements.txt`, the synthetic input dataset, and test results.

## 15. Implementation sequence

Build the system in this order to minimize rework.

1. Define the output schema first. Finalize field names, required values, limits, and exact counts.

2. Create the synthetic company profile. Ensure metrics and constraints are internally consistent enough for strategic analysis.

3. Write and version the prompt architecture. Separate the system prompt, strategy procedure, and few-shot examples.

4. Implement the Pydantic validator and unit tests. Test invalid cases before integrating the LLM.

5. Connect the Groq API. Add structured generation, timeouts, and safe error handling.

6. Add logging and the command-line interface. Keep execution reproducible and easy to review.

7. Run the end-to-end test. Save the exact validated response and inspect its strategic quality.

8. Package the submission. Include the required three deliverables and a concise setup guide.

## 16. Scope boundaries and risks

Included in the MVP: synthetic data, one LLM provider, one model configuration, prompt orchestration, strict JSON output, validation, logging, and automated tests.

Not included: a web dashboard, live CRM integration, real customer analytics, multi-agent orchestration, external marketing execution, or claims of guaranteed revenue improvement.

Key risks are model availability, unsupported structured-output features, inconsistent strategic recommendations, token limits, and rate limiting. Mitigate them through schema-first development, model capability checks, bounded retries, deterministic validation, and transparent assumptions.

Final engineering principle: the LLM proposes the strategy; the application enforces the contract. The system is successful only when it produces a strategically useful report that is also structurally valid, auditable, and reproducible.
