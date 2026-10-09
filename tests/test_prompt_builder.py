import json
from src.prompt_builder import build_messages

def test_build_messages():
    company_data = {"name": "TestCompany"}
    messages = build_messages(company_data)
    
    assert len(messages) >= 3
    assert messages[0]["role"] == "system"
    assert "Output Schema" in messages[0]["content"]
    assert messages[-1]["role"] == "user"
    assert json.loads(messages[-1]["content"]) == company_data
