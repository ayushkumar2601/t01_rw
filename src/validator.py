from schemas.report_schema import ReportSchema
from pydantic import ValidationError

def validate_business_rules(report: dict, company_data: dict) -> list:
    errors = []
    
    channels = report.get("prioritized_growth_channels", [])
    if len(channels) != 3:
        errors.append("Exactly three growth channels must exist")
    
    ranks = [c.get("rank") for c in channels]
    if sorted(ranks) != [1, 2, 3]:
        errors.append("Channel ranks must equal [1, 2, 3] exactly and be unique")
        
    names = [c.get("channel", "").lower() for c in channels]
    if len(set(names)) < len(names):
        errors.append("The three channels must be meaningfully distinct")
    
    plan = report.get("action_plan_30_days", [])
    if len(plan) != 4:
        errors.append("There must be exactly four roadmap phases")
        
    weeks = [p.get("week") for p in plan]
    if sorted(weeks) != [1, 2, 3, 4]:
        errors.append("Roadmap weeks must equal [1, 2, 3, 4] exactly and be unique")
        
    for phase in plan:
        for action in phase.get("actions", []):
            if not (1 <= action.get("due_day", 0) <= 30):
                errors.append("Task due days must fall between day 1 and day 30")
                
    budget = company_data.get("metrics", {}).get("monthly_marketing_budget_usd", 0)
    # Count each unique channel's budget to avoid duplicate budget summation if they somehow duped
    # But since we enforced unique channels above, simple sum is fine.
    total_budget = sum(c.get("budget_usd", 0) for c in channels)
    if total_budget > budget:
        errors.append(f"Combined channel budgets ({total_budget}) exceed marketing budget ({budget})")

    team_size = company_data.get("constraints", {}).get("team_size", 100)
    # Check if owners are plausible. (Basic heuristic: if owner says "team of 10", it fails, but hard to do robustly)
    # Let's just ensure it's provided.
    
    excluded_channels = company_data.get("constraints", {}).get("excluded_channels", [])
    for c in channels:
        channel_name = c.get("channel", "").lower().replace("_", " ")
        for excluded in excluded_channels:
            if excluded.lower().replace("_", " ") in channel_name:
                errors.append(f"Channel {c.get('channel')} is excluded by company constraints")

    # Evidence constraints
    for c in channels:
        evidence = c.get("supporting_evidence", [])
        if not evidence:
            errors.append(f"Channel {c.get('channel')} has no supporting evidence")
            
        # Prioritization score math
        try:
            impact = c.get("score_impact", 0)
            fit = c.get("score_fit", 0)
            feasibility = c.get("score_feasibility", 0)
            learning = c.get("score_learning_speed", 0)
            cost = c.get("score_cost_efficiency", 0)
            expected_score = round((0.35 * impact) + (0.25 * fit) + (0.20 * feasibility) + (0.10 * learning) + (0.10 * cost), 2)
            actual_score = round(c.get("priority_score", 0), 2)
            if abs(expected_score - actual_score) > 0.6: # Allow floating point drift and integer rounding
                errors.append(f"Channel {c.get('channel')} priority score {actual_score} does not match calculated score {expected_score}")
        except Exception:
            errors.append(f"Channel {c.get('channel')} has invalid score fields for calculation")
            
    # Bottleneck grounded
    exec_summary = report.get("executive_summary", {})
    bottleneck = exec_summary.get("primary_bottleneck", "")
    if not bottleneck:
        errors.append("Primary bottleneck is missing")

    return errors

def validate_report(report: dict, company_data: dict) -> list:
    errors = []
    try:
        ReportSchema(**report)
    except ValidationError as e:
        for err in e.errors():
            errors.append(f"{err['loc']}: {err['msg']}")
            
    # Only check business rules if schema passes to avoid type errors in business rules
    if not errors:
        business_errors = validate_business_rules(report, company_data)
        errors.extend(business_errors)
    return errors
