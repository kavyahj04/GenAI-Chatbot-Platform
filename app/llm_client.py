import asyncio
from typing import List, Tuple, Dict, Any

from openai import OpenAI

from .config import get_settings


settings = get_settings()
_client = OpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
)


ChatMessageDict = Dict[str, str]


def generate_completion(
    messages: List[ChatMessageDict],
    model: str,
    temperature: float,
    max_tokens: int,
) -> Tuple[str, Dict[str, Any]]:
    """
    Call the OpenAI chat completion API and return text plus basic usage metadata.
    """
    response = _client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    choice = response.choices[0]
    text = choice.message.content or ""

    usage = {
        "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
        "completion_tokens": response.usage.completion_tokens if response.usage else None,
        "total_tokens": response.usage.total_tokens if response.usage else None,
        "id": response.id,
    }

    return text, usage


async def generate_completion_async(
    messages: List[ChatMessageDict],
    model: str,
    temperature: float,
    max_tokens: int,
) -> Tuple[str, Dict[str, Any]]:
    """
    Async wrapper — runs the blocking OpenAI call in a thread pool so
    the event loop is not blocked during the LLM request.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        lambda: generate_completion(messages, model, temperature, max_tokens),
    )

