from llm.openai import call_openai
from llm.anthropic import call_anthropic
import logging

def call_llm(messages: list[dict], system_message: str = None, model: str = "gpt-4o", max_tokens: int = 1024, provider: str = "openai"):
    logging.info(f"[LLM] Calling \n Provider: {provider} \n Model: {model} \n Messages: {messages} \n System Message: {system_message} \n Max Tokens: {max_tokens}")
    if provider == "openai":
        return call_openai(messages=messages, 
                           system_message=system_message, 
                           model=model, 
                           max_tokens=max_tokens)
    elif provider == "anthropic":
        return call_anthropic(messages=messages, 
                             system_message=system_message, 
                             model=model, 
                             max_tokens=max_tokens)
    else:
        raise ValueError(f"Invalid provider: {provider}")