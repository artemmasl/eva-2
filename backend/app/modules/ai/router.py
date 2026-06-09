import asyncio
import json
import logging
import uuid
from typing import AsyncIterator

from fastapi import APIRouter, Cookie, Request, Response
from fastapi.responses import StreamingResponse

from app.modules.ai.repository import append_message, clear_history, get_history
from app.modules.ai.schemas import ChatHistorySchema, ChatRequest
from app.modules.ai.tools import TOOLS, execute_tool
from app.modules.ai.yandex import chat_completion, chat_completion_stream, is_configured

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["ai"])

SESSION_COOKIE = "eva_ai_session"
SESSION_MAX_AGE = 60 * 60 * 24 * 90  # 90 days
MAX_TOOL_ITERATIONS = 4

SYSTEM_PROMPT = (
    "Ты — AI-помощник на сайте застройщика недвижимости. "
    "Помогаешь подобрать квартиру, парковку, кладовку или коммерцию и отвечаешь на вопросы о жилых комплексах. "
    "Отвечай на русском, дружелюбно и кратко. "
    "Для подбора вариантов и фактов о квартирах ВСЕГДА используй доступные инструменты, "
    "не выдумывай цены, площади, адреса и наличие. "
    "Если пользователь ссылается на 'это/эту/этот/данный' объект, а в контексте есть space_id — "
    "сразу вызови get_space_details с этим space_id и не переспрашивай ID. "
    "Если в контексте есть complex_id — по умолчанию ищи варианты в этом ЖК. "
    "Можешь рассказывать о расположении: адрес, район, метро и время до метро есть в данных. "
    "Найденные варианты карточками покажет интерфейс — не дублируй длинными списками характеристик, "
    "дай короткий комментарий и предложи перейти к карточкам. "
    "Если данных не нашлось — честно скажи и предложи изменить критерии. "
    "Цены указывай в рублях. Не используй разметку Markdown-таблицами."
)


def _build_context_note(request: ChatRequest) -> str | None:
    context = request.context

    if context is None:
        return None

    parts: list[str] = []

    if context.complex_name:
        note = f"ЖК «{context.complex_name}»"
        if context.complex_id:
            note += f" (complex_id={context.complex_id})"
        parts.append(note)
    elif context.complex_id:
        parts.append(f"complex_id={context.complex_id}")

    if context.space_id:
        parts.append(f"открыта квартира space_id={context.space_id}")

    if context.page:
        parts.append(f"страница: {context.page}")

    if not parts:
        return None

    return "Контекст: пользователь сейчас смотрит " + "; ".join(parts) + "."


def _build_model_messages(history: list[dict], request: ChatRequest) -> list[dict]:
    system_content = SYSTEM_PROMPT
    context_note = _build_context_note(request)

    if context_note:
        system_content += "\n" + context_note

    messages: list[dict] = [{"role": "system", "content": system_content}]

    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})

    messages.append({"role": "user", "content": request.message})

    return messages


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


MAX_CARDS = 6


def _collect_cards(name: str, result: str, cards: list[dict], seen: set[str]) -> None:
    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        return

    items: list[dict] = []

    if name == "search_spaces" and isinstance(parsed, dict):
        items = parsed.get("items", [])
    elif name == "get_space_details" and isinstance(parsed, dict) and parsed.get("id"):
        items = [parsed]

    for item in items:
        item_id = item.get("id")
        if not item_id or item_id in seen or len(cards) >= MAX_CARDS:
            continue
        seen.add(item_id)
        cards.append(item)


async def _resolve_tools(messages: list[dict]) -> tuple[bool, str | None, list[dict]]:
    """Run the tool-calling loop (non-streaming).

    Returns (used_tools, direct_answer, cards). direct_answer is set only when
    the model answered immediately without calling any tool. cards holds the
    space items returned by tools for the UI to render.
    """
    used_tools = False
    cards: list[dict] = []
    seen: set[str] = set()

    for _ in range(MAX_TOOL_ITERATIONS):
        message = await chat_completion(messages, TOOLS)
        tool_calls = message.get("tool_calls")

        if not tool_calls:
            return used_tools, message.get("content") or "", cards

        used_tools = True
        messages.append(
            {
                "role": "assistant",
                "content": message.get("content") or "",
                "tool_calls": tool_calls,
            }
        )

        for tool_call in tool_calls:
            function = tool_call.get("function", {})
            name = function.get("name", "")
            result = await execute_tool(name, function.get("arguments", ""))
            _collect_cards(name, result, cards, seen)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.get("id", ""),
                    "content": result,
                }
            )

    return used_tools, None, cards


async def _chunk_text(text: str) -> AsyncIterator[str]:
    words = text.split(" ")

    for index, word in enumerate(words):
        yield word if index == 0 else " " + word
        await asyncio.sleep(0.015)


async def _generate(session_id: str, request: ChatRequest) -> AsyncIterator[str]:
    if not is_configured():
        yield _sse({"type": "error", "text": "AI не настроен: задайте YANDEX_FOLDER_ID и YANDEX_API_KEY."})
        return

    history = await get_history(session_id)
    messages = _build_model_messages(history, request)

    await append_message(session_id, "user", request.message)

    full_answer = ""

    cards: list[dict] = []

    try:
        used_tools, direct_answer, cards = await _resolve_tools(messages)

        if used_tools:
            async for delta in chat_completion_stream(messages):
                full_answer += delta
                yield _sse({"type": "delta", "text": delta})
        else:
            async for delta in _chunk_text(direct_answer or ""):
                full_answer += delta
                yield _sse({"type": "delta", "text": delta})
    except Exception:  # noqa: BLE001 - surface a friendly error to the client
        logger.exception("AI chat failed")
        yield _sse({"type": "error", "text": "Не удалось получить ответ. Попробуйте позже."})
        return

    if cards:
        yield _sse({"type": "cards", "items": cards})

    if full_answer.strip():
        await append_message(session_id, "assistant", full_answer)

    yield _sse({"type": "done"})


@router.post("/chat")
async def chat(
    request: ChatRequest,
    eva_ai_session: str | None = Cookie(default=None),
) -> StreamingResponse:
    session_id = eva_ai_session or uuid.uuid4().hex

    response = StreamingResponse(
        _generate(session_id, request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
    response.set_cookie(
        key=SESSION_COOKIE,
        value=session_id,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
    )

    return response


@router.get("/history", response_model=ChatHistorySchema)
async def history(eva_ai_session: str | None = Cookie(default=None)) -> ChatHistorySchema:
    session_id = eva_ai_session or uuid.uuid4().hex
    messages = await get_history(session_id) if eva_ai_session else []

    return ChatHistorySchema(session_id=session_id, messages=messages)


@router.delete("/history")
async def reset_history(
    response: Response,
    eva_ai_session: str | None = Cookie(default=None),
) -> dict[str, str]:
    if eva_ai_session:
        await clear_history(eva_ai_session)

    return {"status": "ok"}
