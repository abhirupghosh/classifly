import time
import anthropic
import dotenv
import os
import logging
import backoff

dotenv.load_dotenv()

anthropic_client = anthropic.Anthropic(
  api_key=os.environ.get("ANTHROPIC_API_KEY"),
  base_url="https://anthropic.helicone.ai",
  default_headers={
    "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}",
  },
)

@backoff.on_exception(backoff.expo, Exception, max_tries=10, base=2, factor=1, max_value=60)
def call_anthropic(messages: list[dict], system_message: str = None, model: str = "claude-3-5-sonnet-20241022", max_tokens: int = 1024):
    logging.info(f"[ANTHROPIC] Calling \n Model: {model} \n Messages: {messages} \n System Message: {system_message} \n Max Tokens: {max_tokens}")
    start_time = time.time()
    if system_message:
        message = anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            system=system_message,
        )
    else:
        message = anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
        )
    end_time = time.time()
    logging.info(f"[ANTHROPIC] Response \n Content: {message.content} \n Usage: {message.usage} \n Time: {end_time - start_time}s")
    return message.content[0].text
