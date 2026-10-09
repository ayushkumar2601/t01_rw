import argparse
import json
import sys
import hashlib
import time
from src.prompt_builder import build_messages
from src.groq_client import generate_report, GroqClientError
from src.validator import validate_report
from src.logger import log_execution
from src.config import PROMPT_VERSION, GROQ_MODEL

def run_generation(messages, company_data, input_hash):
    start_time = time.time()
    try:
        result = generate_report(messages)
    except GroqClientError as e:
        log_execution(
            prompt_version=PROMPT_VERSION,
            requested_model=GROQ_MODEL,
            input_hash=input_hash,
            status="error",
            error_type=e.error_type
        )
        print(f"Groq API Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    latency = time.time() - start_time
    report = result["content"]
    
    validation_errors = validate_report(report, company_data)
    
    if validation_errors:
        log_execution(
            prompt_version=PROMPT_VERSION,
            requested_model=GROQ_MODEL,
            input_hash=input_hash,
            status="validation_failed",
            latency=latency,
            returned_model=result.get("returned_model", ""),
            token_usage=result.get("usage", {}),
            validation_errors=validation_errors,
            error_type="validation_error"
        )
        return False, validation_errors, messages, latency
        
    return True, report, result, latency

def main():
    parser = argparse.ArgumentParser(description="LLM Brain B2B SaaS Growth Strategy")
    parser.add_argument("--input", required=True, help="Input JSON file containing company context")
    parser.add_argument("--output", required=True, help="Output JSON file for the report")
    parser.add_argument("--print-prompt", action="store_true", help="Print the assembled prompt and exit")
    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            input_content = f.read()
            company_data = json.loads(input_content)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
        
    input_hash = hashlib.sha256(input_content.encode("utf-8")).hexdigest()

    try:
        messages = build_messages(company_data)
    except Exception as e:
        print(f"Error building prompt: {e}", file=sys.stderr)
        sys.exit(1)

    if args.print_prompt:
        print(json.dumps(messages, indent=2))
        sys.exit(0)

    success, result_data, api_result, latency = run_generation(messages, company_data, input_hash)
    
    if not success:
        print("Validation failed, attempting corrective generation...", file=sys.stderr)
        validation_errors = result_data
        
        corrective_msg = {
            "role": "user",
            "content": "Your previous response failed validation with the following errors:\n" + 
                       "\n".join(validation_errors) + 
                       "\nPlease provide a corrected, complete JSON object."
        }
        
        messages.append(corrective_msg)
        
        success2, result_data2, api_result2, latency2 = run_generation(messages, company_data, input_hash)
        if not success2:
            print("Corrective generation failed validation:", file=sys.stderr)
            for err in result_data2:
                print(f" - {err}", file=sys.stderr)
            sys.exit(1)
        
        result_data = result_data2
        api_result = api_result2
        latency += latency2

    report = result_data

    try:
        with open(args.output, "w") as f:
            f.write(json.dumps(report, indent=2))
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

    log_execution(
        prompt_version=PROMPT_VERSION,
        requested_model=GROQ_MODEL,
        input_hash=input_hash,
        status="success",
        latency=latency,
        returned_model=api_result.get("returned_model", ""),
        token_usage=api_result.get("usage", {}),
        output_path=args.output
    )
    
    print(f"Successfully generated growth strategy report to {args.output}")

if __name__ == "__main__":
    main()
