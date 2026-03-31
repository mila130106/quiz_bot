import g4f
import g4f.Provider
import json
import logging
import time
import traceback
import asyncio
from g4f.client import AsyncClient

logger = logging.getLogger(__name__)

# Providers tried in order — fastest/most reliable first.
# Each gets PROVIDER_TIMEOUT seconds before we move on.
PROVIDER_TIMEOUT = 30
PROVIDERS = [
    (g4f.Provider.PollinationsAI, "openai-fast"),
    (g4f.Provider.DeepInfra,      g4f.Provider.DeepInfra.default_model),
    (g4f.Provider.Groq,           g4f.Provider.Groq.default_model),
]


def _parse_response(text: str) -> list:
    text = text.replace("```json", "").replace("```", "").strip()
    start = text.find('[')
    end = text.rfind(']') + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON array in response")
    questions = json.loads(text[start:end])
    # AI returns answer as a letter ("A","B","C","D") but db_operations
    # compares option text directly. Resolve letter → actual option text.
    letter_map = {"A": 0, "B": 1, "C": 2, "D": 3}
    for q in questions:
        answer = q.get("answer", "")
        if answer in letter_map:
            idx = letter_map[answer]
            options = q.get("options", [])
            if idx < len(options):
                q["answer"] = options[idx]
    return questions


async def generate_quiz_ai(topic, count):
    prompt = (
        f"Згенеруй професійний IT квіз про '{topic}' українською мовою. "
        f"Поверни ТІЛЬКИ JSON масив: "
        f"[{{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"answer\": \"A\"}}]. "
        f"Рівно {count} питань. Відповіді мають бути короткими та зрозумілими українською."
    )

    logger.info("[AI] Starting generation: topic='%s', count=%d", topic, count)
    logger.debug("[AI] Prompt: %s", prompt)

    client = AsyncClient()
    total_start = time.monotonic()

    for provider, model in PROVIDERS:
        provider_name = provider.__name__
        logger.info("[AI] Trying provider %s / model %s (timeout=%ds)...", provider_name, model, PROVIDER_TIMEOUT)
        start_time = time.monotonic()
        try:
            response = await asyncio.wait_for(
                client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    provider=provider,
                ),
                timeout=PROVIDER_TIMEOUT,
            )
            elapsed = time.monotonic() - start_time
            text = response.choices[0].message.content or ""
            logger.debug("[AI] %s raw response (%d chars): %s", provider_name, len(text), text[:500])

            parsed = _parse_response(text)
            logger.info("[AI] %s succeeded: parsed %d question(s) in %.2fs (total %.2fs)",
                        provider_name, len(parsed), elapsed, time.monotonic() - total_start)
            return parsed

        except asyncio.TimeoutError:
            logger.warning("[AI] %s timed out after %ds, trying next provider...", provider_name, PROVIDER_TIMEOUT)
        except Exception as exc:
            elapsed = time.monotonic() - start_time
            logger.warning("[AI] %s failed after %.2fs — %s: %s", provider_name, elapsed, type(exc).__name__, exc)
            logger.debug("[AI] %s traceback:\n%s", provider_name, traceback.format_exc())

    logger.error("[AI] All providers failed after %.2fs. Using fallback.", time.monotonic() - total_start)
    return [
        {"question": f"Яке основне призначення {topic}?", "options": ["Розробка", "Тестування", "Дизайн", "Маркетинг"], "answer": "Розробка"},
        {"question": f"Який синтаксис правильний в {topic}?", "options": ["Варіант А", "Варіант Б", "Варіант В", "Варіант Г"], "answer": "Варіант А"},
        {"question": f"Чи використовується {topic} для backend розробки?", "options": ["Так", "Ні", "Інколи", "Ніколи"], "answer": "Так"}
    ][:count]
