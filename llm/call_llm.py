from llm.openai import call_openai
from llm.anthropic import call_anthropic
import logging

def call_llm(messages: list[dict], system_message: str = None, model: str = "gpt-4o", max_tokens: int = 1024, provider: str = "openai"):
    """
    Call the specified LLM provider with the given parameters.

    Args:
        messages (list[dict]): List of message dictionaries.
        system_message (str, optional): System message to set context.
        model (str, optional): The model to use. Defaults to "gpt-4o".
        max_tokens (int, optional): Maximum number of tokens in the response. Defaults to 1024.
        provider (str, optional): The LLM provider to use. Defaults to "openai".

    Returns:
        str: The generated text response from the model.

    Raises:
        ValueError: If an invalid provider is specified.
    """
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
