import logging
import json
import os
import uuid
from datetime import datetime, timezone

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("llm_brain")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

def log_execution(
    prompt_version: str,
    requested_model: str,
    input_hash: str,
    status: str,
    latency: float = 0.0,
    returned_model: str = "",
    token_usage: dict = None,
    validation_errors: list = None,
    output_path: str = "",
    error_type: str = ""
):
    run_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "run_id": run_id,
        "timestamp": now,
        "prompt_version": prompt_version,
        "requested_model": requested_model,
        "returned_model": returned_model,
        "input_hash": input_hash,
        "status": status,
        "latency": latency,
        "token_usage": token_usage or {},
        "validation_errors": validation_errors or [],
        "output_path": output_path,
        "error_type": error_type
    }
    with open("logs/runs.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")
    if status == "success":
        logger.info(f"Run {run_id} completed successfully.")
    else:
        logger.error(f"Run {run_id} failed: {error_type}")
