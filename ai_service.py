import g4f
import json
import asyncio

async def generate_quiz_ai(topic):
    prompt = f"Generate a professional IT quiz about '{topic}' in English. Return ONLY a JSON array: [{{'question': '...', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'}}]. Exactly 3 questions."
    
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.replace("```json", "").replace("```", "").strip()
        start = text.find('[')
        end = text.rfind(']') + 1
        return json.loads(text[start:end])
    except:
        return [
            {"question": f"What is the main purpose of {topic}?", "options": ["Development", "Testing", "Design", "Marketing"], "answer": "Development"},
            {"question": f"Which syntax is correct in {topic}?", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "Option A"},
            {"question": f"Is {topic} used for backend engineering?", "options": ["Yes", "No", "Sometimes", "Never"], "answer": "Yes"}
        ]