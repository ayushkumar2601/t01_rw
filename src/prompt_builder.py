import json
from schemas.report_schema import ReportSchema

def load_text(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def build_messages(company_data: dict) -> list:
    system_prompt = load_text("prompts/system.md")
    strategy_procedure = load_text("prompts/strategy_procedure.md")
    
    with open("prompts/few_shot_examples.json", "r") as f:
        few_shots = json.load(f)

    json_schema = ReportSchema.model_json_schema()
    
    messages = [
        {
            "role": "system",
            "content": f"{system_prompt}\n\n{strategy_procedure}\n\nOutput Schema:\n{json.dumps(json_schema, indent=2)}"
        }
    ]

    for example in few_shots:
        messages.append({
            "role": "user",
            "content": json.dumps(example["input"])
        })
        messages.append({
            "role": "assistant",
            "content": json.dumps(example["output"])
        })

    messages.append({
        "role": "user",
        "content": json.dumps(company_data)
    })

    return messages
