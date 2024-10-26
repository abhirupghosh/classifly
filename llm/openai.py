import time
import anthropic
import dotenv
import os
import logging
import backoff
import openai
dotenv.load_dotenv()

openai_client = openai.OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
  base_url="https://openai.helicone.ai",
  default_headers={
    "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}",
  },
)

@backoff.on_exception(backoff.expo, Exception, max_tries=10, base=2, factor=1, max_value=60)
def call_openai(messages: list[dict], system_message: str = None, model: str = "gpt-4o", max_tokens: int = 1024):
    logging.info(f"[OPENAI] Calling \n Model: {model} \n Messages: {messages} \n System Message: {system_message} \n Max Tokens: {max_tokens}")
    start_time = time.time()
    if system_message:
        messages.insert(0, {"role": "system", "content": system_message})
        completion =openai_client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages
        )
    else:
        completion = openai_client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages
        )
    end_time = time.time()
    response = completion.choices[0].message.content
    logging.info(f"[OPENAI] Response \n Content: {response} \n Usage: {completion.usage} \n Time: {end_time - start_time}s")
    return response