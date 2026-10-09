import pytest
from pydantic import ValidationError
from schemas.report_schema import ReportSchema

def valid_data():
    return {
        "executive_summary": {
            "company_name": "Test",
            "primary_bottleneck": "Test",
            "key_findings": ["Test"],
            "strategic_thesis": "Test",
            "primary_30_day_objective": "Test",
            "assumptions": ["Test"]
        },
        "prioritized_growth_channels": [
            {
                "rank": 1,
                "channel": "C1",
                "priority_score": 50,
                "rationale": "R1",
                "supporting_evidence": ["E1"],
                "system_to_build": "S1",
                "leading_kpi": "K1",
                "target": "T1",
                "budget_usd": 100,
                "time_to_signal_days": 10,
                "risks": ["Risk1"],
                "score_impact": 50,
                "score_fit": 50,
                "score_feasibility": 50,
                "score_learning_speed": 50,
                "score_cost_efficiency": 50
            },
            {
                "rank": 2,
                "channel": "C2",
                "priority_score": 50,
                "rationale": "R2",
                "supporting_evidence": ["E2"],
                "system_to_build": "S2",
                "leading_kpi": "K2",
                "target": "T2",
                "budget_usd": 100,
                "time_to_signal_days": 10,
                "risks": ["Risk2"],
                "score_impact": 50,
                "score_fit": 50,
                "score_feasibility": 50,
                "score_learning_speed": 50,
                "score_cost_efficiency": 50
            },
            {
                "rank": 3,
                "channel": "C3",
                "priority_score": 50,
                "rationale": "R3",
                "supporting_evidence": ["E3"],
                "system_to_build": "S3",
                "leading_kpi": "K3",
                "target": "T3",
                "budget_usd": 100,
                "time_to_signal_days": 10,
                "risks": ["Risk3"],
                "score_impact": 50,
                "score_fit": 50,
                "score_feasibility": 50,
                "score_learning_speed": 50,
                "score_cost_efficiency": 50
            }
        ],
        "action_plan_30_days": [
            {
                "week": 1,
                "theme": "Th1",
                "objective": "Obj1",
                "actions": [
                    {"task": "T1", "owner": "O1", "due_day": 5, "success_metric": "SM1", "deliverable": "D1"}
                ]
            },
            {
                "week": 2,
                "theme": "Th2",
                "objective": "Obj2",
                "actions": [
                    {"task": "T2", "owner": "O2", "due_day": 10, "success_metric": "SM2", "deliverable": "D2"}
                ]
            },
            {
                "week": 3,
                "theme": "Th3",
                "objective": "Obj3",
                "actions": [
                    {"task": "T3", "owner": "O3", "due_day": 15, "success_metric": "SM3", "deliverable": "D3"}
                ]
            },
            {
                "week": 4,
                "theme": "Th4",
                "objective": "Obj4",
                "actions": [
                    {"task": "T4", "owner": "O4", "due_day": 20, "success_metric": "SM4", "deliverable": "D4"}
                ]
            }
        ]
    }

def test_valid_schema():
    report = ReportSchema(**valid_data())
    assert report.executive_summary.company_name == "Test"

def test_missing_fields():
    data = valid_data()
    del data["executive_summary"]["company_name"]
    with pytest.raises(ValidationError):
        ReportSchema(**data)

def test_extra_fields_forbidden():
    data = valid_data()
    data["extra_field"] = "not_allowed"
    with pytest.raises(ValidationError):
        ReportSchema(**data)

def test_bool_rejected_for_int():
    data = valid_data()
    data["prioritized_growth_channels"][0]["rank"] = True
    with pytest.raises(ValidationError):
        ReportSchema(**data)

def test_empty_strings_rejected():
    data = valid_data()
    data["executive_summary"]["company_name"] = ""
    with pytest.raises(ValidationError):
        ReportSchema(**data)

def test_negative_budget():
    data = valid_data()
    data["prioritized_growth_channels"][0]["budget_usd"] = -10
    with pytest.raises(ValidationError):
        ReportSchema(**data)

def test_channel_count():
    data = valid_data()
    data["prioritized_growth_channels"].pop() # Only 2 channels
    with pytest.raises(ValidationError):
        ReportSchema(**data)
