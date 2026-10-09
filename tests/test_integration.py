import pytest
from unittest.mock import patch, MagicMock
from src.groq_client import generate_report, GroqClientError

@patch('src.groq_client.client.chat.completions.create')
def test_generate_report_success(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"test": "data"}'
    mock_response.model = "mock-model"
    mock_response.usage.model_dump.return_value = {"total_tokens": 100}
    mock_create.return_value = mock_response

    result = generate_report([{"role": "user", "content": "test"}])
    assert result["content"] == {"test": "data"}
    assert result["returned_model"] == "mock-model"
    assert result["usage"] == {"total_tokens": 100}

@patch('src.groq_client.client.chat.completions.create')
def test_generate_report_invalid_json(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = 'invalid json'
    mock_create.return_value = mock_response

    with pytest.raises(GroqClientError) as exc_info:
        generate_report([{"role": "user", "content": "test"}])
    assert "not valid JSON" in str(exc_info.value)

import os
from src.prompt_builder import build_messages

@pytest.mark.integration
def test_live_groq_call():
    if not os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY") == "dummy":
        pytest.skip("GROQ_API_KEY not set, skipping live integration test")
        
    company_data = {"name": "TestCompany"}
    messages = build_messages(company_data)
    
    result = generate_report(messages)
    assert "content" in result
    assert "returned_model" in result
