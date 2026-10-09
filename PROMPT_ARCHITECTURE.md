# Prompt Architecture

## Project Objective and Scope
The goal of this system is to generate a structured B2B SaaS growth strategy report using a deterministic prompt architecture and an LLM capable of structured JSON generation (Llama 3.3 70B via Groq API). The output must strictly adhere to a Pydantic-defined JSON schema representing prioritized channels and a 30-day action plan.

## System Persona and Behavioral Constraints
Defined in `prompts/system.md`. The persona is a senior B2B SaaS growth strategist. Behavioral constraints force the model to focus on evidence-based recommendations, sustainable growth, and actionable roadmaps instead of vanity metrics or unsupported claims.

## Context Injection and Synthetic Data
The company data (e.g., `data/saas_company.json`) is read and formatted as a JSON string, then passed as the final user message. It separates facts from the instruction layers.

## Reasoning Procedure and Scoring Rubric
Defined in `prompts/strategy_procedure.md`. The model uses a 5-factor scoring rubric (impact, fit, execution, learning speed, cost) to evaluate and rank channels. It separates internal procedure instructions from output formatting.

## Few-shot Example Design
Defined in `prompts/few_shot_examples.json`. Shows a mapping from a small fictional company context to a complete, valid JSON response. This provides in-context learning for the exact structure and tone required.

## Output Schema and Strict Validation
The JSON Schema is dynamically generated from Pydantic models (`schemas/report_schema.py`) and injected into the system prompt. Pydantic is then used post-generation to enforce type checking and structural completeness, along with a business rule validator that checks counts, bounds, and consistency.

## Prompt Assembly Order and Precedence
1. System prompt + Strategy procedure + JSON Schema
2. Few-shot input (User)
3. Few-shot output (Assistant)
4. Actual company data (User)

## Groq Structured-Output Strategy
The application requests `response_format={"type": "json_object"}` from the Groq API and relies on the injected JSON Schema and Pydantic validation to enforce strictness, as standard JSON mode only guarantees valid syntax.

## Hallucination Mitigation and Bounded Recovery
The strict schema with `extra="forbid"` and the explicit business rules checker detect invalid or hallucinated structures.
If the API returns invalid or business-rule violating JSON, the system makes **one corrective-generation attempt** using the recorded validation errors as feedback.

## Testing and Known Limitations
Tested using Pydantic unit tests and mock-based generation tests. Known limitation: Without tool calling, the LLM cannot query live systems, so it relies entirely on the provided static synthetic metrics.
