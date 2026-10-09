from src.validator import validate_business_rules

def valid_report():
    return {
        "executive_summary": {
            "primary_bottleneck": "Testing bottleneck"
        },
        "prioritized_growth_channels": [
            {"channel": "c1", "rank": 1, "budget_usd": 100, "rationale": "r1", "supporting_evidence": ["e1"], "priority_score": 50, "score_impact": 50, "score_fit": 50, "score_feasibility": 50, "score_learning_speed": 50, "score_cost_efficiency": 50},
            {"channel": "c2", "rank": 2, "budget_usd": 100, "rationale": "r2", "supporting_evidence": ["e2"], "priority_score": 50, "score_impact": 50, "score_fit": 50, "score_feasibility": 50, "score_learning_speed": 50, "score_cost_efficiency": 50},
            {"channel": "c3", "rank": 3, "budget_usd": 100, "rationale": "r3", "supporting_evidence": ["e3"], "priority_score": 50, "score_impact": 50, "score_fit": 50, "score_feasibility": 50, "score_learning_speed": 50, "score_cost_efficiency": 50}
        ],
        "action_plan_30_days": [
            {"week": 1, "actions": [{"task": "t", "owner": "o", "due_day": 5, "success_metric": "s", "deliverable": "d"}]},
            {"week": 2, "actions": []},
            {"week": 3, "actions": []},
            {"week": 4, "actions": []}
        ]
    }

def valid_company_data():
    return {
        "metrics": {"monthly_marketing_budget_usd": 1000},
        "constraints": {"team_size": 10, "excluded_channels": ["bad_channel"]}
    }

def test_business_rules_valid():
    errors = validate_business_rules(valid_report(), valid_company_data())
    assert len(errors) == 0

def test_invalid_channel_ranks():
    report = valid_report()
    report["prioritized_growth_channels"][2]["rank"] = 4
    errors = validate_business_rules(report, valid_company_data())
    assert any("Channel ranks must equal" in e for e in errors)

def test_duplicate_channels():
    report = valid_report()
    report["prioritized_growth_channels"][1]["channel"] = "c1"
    errors = validate_business_rules(report, valid_company_data())
    assert any("meaningfully distinct" in e for e in errors)

def test_budget_exceeded():
    report = valid_report()
    report["prioritized_growth_channels"][0]["budget_usd"] = 900
    errors = validate_business_rules(report, valid_company_data())
    assert any("exceed marketing budget" in e for e in errors)

def test_excluded_channel():
    report = valid_report()
    report["prioritized_growth_channels"][0]["channel"] = "bad_channel strategy"
    errors = validate_business_rules(report, valid_company_data())
    assert any("excluded by company constraints" in e for e in errors)

def test_score_calculation():
    report = valid_report()
    report["prioritized_growth_channels"][0]["priority_score"] = 99
    errors = validate_business_rules(report, valid_company_data())
    assert any("does not match calculated score" in e for e in errors)

def test_missing_bottleneck():
    report = valid_report()
    report["executive_summary"]["primary_bottleneck"] = ""
    errors = validate_business_rules(report, valid_company_data())
    assert any("Primary bottleneck is missing" in e for e in errors)
