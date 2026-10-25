#!/usr/bin/env python3
"""
LLM Brain Test Script
Task 01 — B2B Growth Strategy Data Report Generator

This script runs the 5-layer prompting architecture through the Groq API,
validates the output against the Pydantic schema and business rules,
logs the input and final output, and saves the machine-readable JSON report.
"""

import os
import sys
import json
import time
import hashlib
import argparse
from pathlib import Path

# Add project root to sys.path so imports work regardless of execution directory
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent if CURRENT_DIR.name == "submission" else CURRENT_DIR
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from src.prompt_builder import build_messages
from src.groq_client import generate_report, GroqClientError
from src.validator import validate_report
from src.logger import log_execution
from src.config import GROQ_MODEL, PROMPT_VERSION


def run_pipeline(input_path: Path, output_path: Path, print_prompt: bool = False):
    print("=" * 70)
    print("🧠 LLM Brain — B2B Growth Strategy Pipeline Runner")
    print("=" * 70)

    # 1. Ingest Synthetic SaaS Company Data
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r") as f:
        input_raw = f.read()
        company_data = json.loads(input_raw)

    input_hash = hashlib.sha256(input_raw.encode("utf-8")).hexdigest()
    print(f"📥 [Step 1] Ingested company: {company_data.get('company', {}).get('name', 'Unknown')}")
    print(f"   Input Hash (SHA-256): {input_hash[:16]}...")
    print(f"   Metrics: Churn={company_data.get('metrics', {}).get('monthly_churn_rate_pct')}%, "
          f"Visitors={company_data.get('metrics', {}).get('monthly_website_visitors')}, "
          f"Inbound Leads={company_data.get('metrics', {}).get('monthly_inbound_leads')}")

    # 2. Assemble 5-Layer Prompt Stack
    try:
        messages = build_messages(company_data)
        print(f"🧩 [Step 2] Assembled {len(messages)} messages (System + CoT + Few-Shot + Context)")
    except Exception as e:
        print(f"❌ Error assembling prompt: {e}", file=sys.stderr)
        sys.exit(1)

    if print_prompt:
        print("\n--- Assembled Prompt Messages ---")
        print(json.dumps(messages, indent=2))
        return

    # 3. Call Groq API (Structured JSON Mode)
    print(f"🚀 [Step 3] Calling Groq API with model: {GROQ_MODEL}...")
    start_time = time.time()
    try:
        api_result = generate_report(messages)
        latency = time.time() - start_time
        print(f"   Inference complete in {latency:.2f}s (Tokens: {api_result.get('usage', {}).get('total_tokens', 'N/A')})")
    except GroqClientError as e:
        print(f"❌ Groq API Error: {e}", file=sys.stderr)
        log_execution(
            prompt_version=PROMPT_VERSION,
            requested_model=GROQ_MODEL,
            input_hash=input_hash,
            status="error",
            error_type=e.error_type
        )
        sys.exit(1)

    report = api_result["content"]

    # 4. Enforce Output Validation (Schema + Deterministic Business Rules)
    print("🛡️  [Step 4] Validating JSON schema and business rules...")
    validation_errors = validate_report(report, company_data)

    if validation_errors:
        print(f"⚠️  Validation failed with {len(validation_errors)} error(s):")
        for err in validation_errors:
            print(f"   - {err}")

        # Corrective feedback attempt
        print("🔄 Attempting bounded corrective generation...")
        messages.append({"role": "assistant", "content": json.dumps(report)})
        error_items = "\n".join(f"- {err}" for err in validation_errors)
        corrective_msg = {
            "role": "user",
            "content": (
                f"Your previous response failed validation with the following specific errors:\n{error_items}\n\n"
                "Please fix these specific errors and provide the corrected, complete JSON object.\n"
                "Ensure each channel's priority_score strictly equals:\n"
                "round((0.35 * score_impact) + (0.25 * score_fit) + (0.20 * score_feasibility) + (0.10 * score_learning_speed) + (0.10 * score_cost_efficiency), 2)."
            )
        }
        messages.append(corrective_msg)

        try:
            start_time2 = time.time()
            api_result2 = generate_report(messages)
            latency += (time.time() - start_time2)
            report = api_result2["content"]
            validation_errors = validate_report(report, company_data)
            if validation_errors:
                print("❌ Corrective attempt also failed validation:", file=sys.stderr)
                for err in validation_errors:
                    print(f"   - {err}", file=sys.stderr)
                log_execution(
                    prompt_version=PROMPT_VERSION,
                    requested_model=GROQ_MODEL,
                    input_hash=input_hash,
                    status="validation_failed",
                    latency=latency,
                    validation_errors=validation_errors,
                    error_type="validation_error"
                )
                sys.exit(1)
            print("✅ Corrective generation succeeded!")
            api_result = api_result2
        except GroqClientError as e:
            print(f"❌ Error during corrective generation: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("✅ Validation PASSED! 100% schema compliant and business-rule sound.")

    # 5. Persist Output & Structured Logging
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    log_execution(
        prompt_version=PROMPT_VERSION,
        requested_model=GROQ_MODEL,
        input_hash=input_hash,
        status="success",
        latency=latency,
        returned_model=api_result.get("returned_model", ""),
        token_usage=api_result.get("usage", {}),
        output_path=str(output_path)
    )

    print(f"💾 [Step 5] Saved verified report to: {output_path}")
    print("=" * 70)
    print("📊 Executive Summary Snapshot:")
    print(f"   Bottleneck: {report.get('executive_summary', {}).get('primary_bottleneck')}")
    print(f"   Thesis:     {report.get('executive_summary', {}).get('strategic_thesis')}")
    print(f"   Prioritized Growth Channels:")
    for ch in report.get("prioritized_growth_channels", []):
        print(f"     #{ch.get('rank')} {ch.get('channel')} (Score: {ch.get('priority_score')}, Budget: ${ch.get('budget_usd')})")
    print("-" * 70)
    print("📅 30-Day 'Systems, Not Campaigns' Action Plan:")
    for phase in report.get("action_plan_30_days", []):
        print(f"   Week {phase.get('week')} ({phase.get('theme')}): {phase.get('objective')}")
        for action in phase.get("actions", []):
            print(f"     • [Day {action.get('due_day')}] {action.get('task')} (Owner: {action.get('owner')}) -> {action.get('deliverable')}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Test and validate LLM Brain B2B Growth Strategy")
    parser.add_argument("--input", default=str(PROJECT_ROOT / "data" / "saas_company.json"),
                        help="Path to synthetic company input JSON (default: data/saas_company.json)")
    parser.add_argument("--output", default=str(CURRENT_DIR / "sample_report.json"),
                        help="Path to save output JSON report (default: submission/sample_report.json)")
    parser.add_argument("--print-prompt", action="store_true",
                        help="Print assembled prompt messages and exit")
    args = parser.parse_args()

    run_pipeline(Path(args.input), Path(args.output), print_prompt=args.print_prompt)


if __name__ == "__main__":
    main()
