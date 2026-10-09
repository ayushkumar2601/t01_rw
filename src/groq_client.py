import json
import time
from groq import Groq, APIError, APIConnectionError, RateLimitError, APITimeoutError, AuthenticationError
from src.config import GROQ_API_KEY, GROQ_MODEL, REQUEST_TIMEOUT_SECONDS, MAX_OUTPUT_TOKENS, MAX_RETRIES

client = Groq(api_key=GROQ_API_KEY, timeout=REQUEST_TIMEOUT_SECONDS)

class GroqClientError(Exception):
    def __init__(self, message, error_type="api_error"):
        super().__init__(message)
        self.error_type = error_type

def generate_report(messages: list) -> dict:
    attempt = 0
    while attempt <= MAX_RETRIES:
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=MAX_OUTPUT_TOKENS,
            )
            if not response.choices or not response.choices[0].message.content:
                raise GroqClientError("Empty response from Groq API", error_type="empty_response")
            
            content = response.choices[0].message.content
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError:
                raise GroqClientError("Groq response is not valid JSON", error_type="invalid_json")

            return {
                "content": parsed_content,
                "returned_model": response.model,
                "usage": response.usage.model_dump() if response.usage else {},
                "attempts": attempt + 1
            }
            
        except AuthenticationError as e:
            raise GroqClientError(f"Authentication Error: {str(e)}", error_type="auth_error")
        except RateLimitError as e:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise GroqClientError(f"Rate Limit Exceeded: {str(e)}", error_type="rate_limit")
            time.sleep(2 ** attempt)
        except (APIConnectionError, APITimeoutError) as e:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise GroqClientError(f"Connection/Timeout Error: {str(e)}", error_type="connection_error")
            time.sleep(2 ** attempt)
        except APIError as e:
            attempt += 1
            if attempt > MAX_RETRIES:
                raise GroqClientError(f"API Error: {str(e)}", error_type="server_error")
            time.sleep(2 ** attempt)
        except GroqClientError:
            raise
        except Exception as e:
            raise GroqClientError(f"Unexpected Error: {str(e)}", error_type="unexpected_error")
