import json
import logging
import time
from openai import AsyncOpenAI
from config.settings import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# OpenAI configuration
MODEL = "gpt-4o-mini"
REQUEST_TIMEOUT = 60

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


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
<<<<<<< HEAD
        f"Згенеруй професійний квіз про '{topic}' українською мовою. "
        f"Поверни ТІЛЬКИ JSON масив: "
        f"[{{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"answer\": \"A\"}}]. "
        f"Рівно {count} питань. Відповіді мають бути короткими та зрозумілими українською."
=======
        f"Згенеруй професійний IT квіз про '{topic}' українською мовою.\n"
        f"ВАЖЛИВО: Поверни РІВНО {count} питань, не більше і не менше!\n"
        f"Формат: JSON масив без додаткового тексту:\n"
        f"[{{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"answer\": \"A\"}}]\n"
        f"Кількість елементів у масиві: {count}. Відповіді короткі українською."
>>>>>>> c9b635a75dc234a3267d2c89df65ff8241fbc1ae
    )

    logger.info("[AI] Starting generation: topic='%s', count=%d", topic, count)
    logger.debug("[AI] Prompt: %s", prompt)

    start_time = time.monotonic()
    max_retries = 2

    for attempt in range(max_retries + 1):
        try:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                timeout=REQUEST_TIMEOUT,
            )
            elapsed = time.monotonic() - start_time
            text = response.choices[0].message.content or ""
            logger.debug("[AI] OpenAI raw response (%d chars): %s", len(text), text[:500])

            parsed = _parse_response(text)

            if len(parsed) == count:
                logger.info("[AI] OpenAI succeeded: parsed %d question(s) in %.2fs", len(parsed), elapsed)
                return parsed
            elif len(parsed) > count:
                logger.info("[AI] Got %d questions, trimming to %d", len(parsed), count)
                return parsed[:count]
            else:
                logger.warning("[AI] Got %d questions, expected %d. Attempt %d/%d",
                             len(parsed), count, attempt + 1, max_retries + 1)
                if attempt == max_retries:
                    logger.info("[AI] Returning %d questions after retries", len(parsed))
                    return parsed

        except Exception as exc:
            elapsed = time.monotonic() - start_time
            logger.error("[AI] OpenAI failed after %.2fs — %s: %s", elapsed, type(exc).__name__, exc)
            break

    logger.error("[AI] Request failed. Using fallback.")
    return [
        {"question": f"Яке основне призначення {topic}?", "options": ["Розробка", "Тестування", "Дизайн", "Маркетинг"], "answer": "Розробка"},
        {"question": f"Який синтаксис правильний в {topic}?", "options": ["Варіант А", "Варіант Б", "Варіант В", "Варіант Г"], "answer": "Варіант А"},
        {"question": f"Чи використовується {topic} для backend розробки?", "options": ["Так", "Ні", "Інколи", "Ніколи"], "answer": "Так"}
    ][:count]
