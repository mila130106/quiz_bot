import g4f
import json
import asyncio

async def generate_quiz_ai(topic):
    prompt = f"Згенеруй професійний IT квіз про '{topic}' українською мовою. Поверни ТІЛЬКИ JSON масив: [{{'question': '...', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'}}]. Рівно 3 питання. Відповіді мають бути короткими та зрозумілими українською."

    try:
        response = await g4f.ChatCompletion.create_async( model=g4f.models.default, messages=[{"role": "user", "content": prompt}],)
        text = response.replace("```json", "").replace("```", "").strip()
        start = text.find('[')
        end = text.rfind(']') + 1
        return json.loads(text[start:end])
    except:
        return [
            {"question": f"Яке основне призначення {topic}?", "options": ["Розробка", "Тестування", "Дизайн", "Маркетинг"], "answer": "Розробка"},
            {"question": f"Який синтаксис правильний в {topic}?", "options": ["Варіант А", "Варіант Б", "Варіант В", "Варіант Г"], "answer": "Варіант А"},
            {"question": f"Чи використовується {topic} для backend розробки?", "options": ["Так", "Ні", "Інколи", "Ніколи"], "answer": "Так"}
        ]