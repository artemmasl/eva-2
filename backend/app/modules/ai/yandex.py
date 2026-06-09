import json
import logging
from typing import AsyncIterator

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

YANDEX_COMPLETIONS_URL = "https://llm.api.cloud.yandex.net/v1/chat/completions"

DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2000


def is_configured() -> bool:
    return bool(settings.yandex_api_key and settings.yandex_folder_id)


def _model_uri() -> str:
    return f"gpt://{settings.yandex_folder_id}/{settings.yandex_model}/latest"


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Api-Key {settings.yandex_api_key}",
        "Content-Type": "application/json",
    }


def _base_payload(messages: list[dict], tools: list[dict] | None) -> dict:
    payload: dict = {
        "model": _model_uri(),
        "messages": messages,
        "temperature": DEFAULT_TEMPERATURE,
        "max_tokens": DEFAULT_MAX_TOKENS,
    }

    if tools:
        payload["tools"] = tools

    return payload


async def chat_completion(
    messages: list[dict],
    tools: list[dict] | None = None,
) -> dict:
    """Single non-streaming completion. Returns the assistant message dict."""
    payload = _base_payload(messages, tools)
    payload["stream"] = False

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(YANDEX_COMPLETIONS_URL, headers=_headers(), json=payload)

        if response.status_code >= 400:
            logger.error("YandexGPT %s error: %s", response.status_code, response.text)

        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]


async def chat_completion_stream(messages: list[dict]) -> AsyncIterator[str]:
    """Streaming completion (no tools). Yields text deltas as they arrive."""
    payload = _base_payload(messages, tools=None)
    payload["stream"] = True

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST", YANDEX_COMPLETIONS_URL, headers=_headers(), json=payload
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if not line or not line.startswith("data:"):
                    continue

                data = line[len("data:"):].strip()

                if data == "[DONE]":
                    break

                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue

                choices = chunk.get("choices") or []

                if not choices:
                    continue

                delta = choices[0].get("delta") or {}
                content = delta.get("content")

                if content:
                    yield content
