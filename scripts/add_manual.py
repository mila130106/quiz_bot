from services.db_operations import save_quiz_to_db

final_quizzes = [
    {
        "title": "Веб-розробка (HTML/CSS)",
        "questions": [
            {"question": "Який тег використовується для внутрішнього CSS?", "options": ["<script>", "<style>", "<link>", "<css>"], "answer": "<style>"},
            {"question": "Що означає CSS?", "options": ["Cascading Style Sheets", "Computer Style System", "Creative Style", "Colorful Sheets"], "answer": "Cascading Style Sheets"},
            {"question": "Яка властивість змінює колір фону?", "options": ["color", "bgcolor", "background-color", "canvas"], "answer": "background-color"}
        ]
    },
    {
        "title": "Програмування Python",
        "questions": [
            {"question": "Як визначити функцію?", "options": ["def func():", "function func():", "create func():", "func():"], "answer": "def func():"},
            {"question": "Який тип має List?", "options": ["Впорядкований і змінюваний", "Невпорядкований", "Незмінний", "Тільки числа"], "answer": "Впорядкований і змінюваний"},
            {"question": "Правильний синтаксис циклу for?", "options": ["for x in y:", "for x > y:", "loop x:", "foreach x:"], "answer": "for x in y:"}
        ]
    },
    {
        "title": "Бази даних SQL",
        "questions": [
            {"question": "Яка команда витягує дані?", "options": ["GET", "SELECT", "EXTRACT", "OPEN"], "answer": "SELECT"},
            {"question": "Як видалити запис?", "options": ["REMOVE", "DELETE", "DROP", "ERASE"], "answer": "DELETE"},
            {"question": "Що означає SQL?", "options": ["Simple Query Lang", "Structured Query Lang", "System Query List", "Standard Quest"], "answer": "Structured Query Lang"}
        ]
    },
    {
        "title": "Основи Git",
        "questions": [
            {"question": "Команда для збереження змін?", "options": ["git push", "git commit -m", "git add", "git save"], "answer": "git commit -m"},
            {"question": "Як перевірити статус?", "options": ["git check", "git info", "git status", "git log"], "answer": "git status"},
            {"question": "Команда для завантаження на GitHub?", "options": ["git send", "git upload", "git push", "git commit"], "answer": "git push"}
        ]
    },
    {
        "title": "Основи кібербезпеки",
        "questions": [
            {"question": "Що таке фішинг?", "options": ["Соціальна інженерія", "Тип вірусу", "Баг апаратури", "Мережевий протокол"], "answer": "Соціальна інженерія"},
            {"question": "Що забезпечує 'HTTPS'?", "options": ["Швидкість", "Шифрування", "Графіка", "Зберігання"], "answer": "Шифрування"},
            {"question": "Для чого використовується Firewall?", "options": ["Моніторинг трафіку", "Очищення вірусів", "Охолодження CPU", "Зберігання паролів"], "answer": "Моніторинг трафіку"}
        ]
    },
    {
        "title": "Вступ до JavaScript",
        "questions": [
            {"question": "Як оголосити змінну?", "options": ["var", "let", "const", "Усе вище"], "answer": "Усе вище"},
            {"question": "Що не є типом даних JS?", "options": ["String", "Boolean", "Float", "Undefined"], "answer": "Float"},
            {"question": "Як вивести сповіщення?", "options": ["msg('Hi')", "alert('Hi')", "print('Hi')", "log('Hi')"], "answer": "alert('Hi')"}
        ]
    },
    {
        "title": "Тестування ПЗ (QA)",
        "questions": [
            {"question": "Що таке баг?", "options": ["Функціонал", "Помилка в коді", "Частина апаратури", "Тест-кейс"], "answer": "Помилка в коді"},
            {"question": "Який тест виконується першим?", "options": ["Модульне тестування", "Системне тестування", "Приймальне", "Бета-тестування"], "answer": "Модульне тестування"},
            {"question": "Що таке 'Black Box' тестування?", "options": ["Тестування без доступу до коду", "Тестування апаратури", "Перегляд коду", "Тест швидкості"], "answer": "Тестування без доступу до коду"}
        ]
    },
    {
        "title": "Основи Data Science",
        "questions": [
            {"question": "Головна бібліотека для даних у Python?", "options": ["Pandas", "Flask", "Django", "Math"], "answer": "Pandas"},
            {"question": "Що означає 'ML'?", "options": ["Machine Learning", "Manual Logic", "Main Link", "Meta Layer"], "answer": "Machine Learning"},
            {"question": "CSV розшифровується як?", "options": ["Comma Separated Values", "Core System", "Code Style", "Central Store"], "answer": "Comma Separated Values"}
        ]
    },
    {
        "title": "Комп'ютерні мережі",
        "questions": [
            {"question": "Порт для HTTP?", "options": ["80", "443", "21", "22"], "answer": "80"},
            {"question": "Що таке IP?", "options": ["Internet Protocol", "Internal Program", "Instant Point", "Input Port"], "answer": "Internet Protocol"},
            {"question": "Пристрій для маршрутизації?", "options": ["Router", "Monitor", "Hub", "Switch"], "answer": "Router"}
        ]
    },
    {
        "title": "Мобільна розробка",
        "questions": [
            {"question": "Мова для Android?", "options": ["Kotlin", "Swift", "C++", "PHP"], "answer": "Kotlin"},
            {"question": "Мова для iOS?", "options": ["Swift", "Java", "Python", "Ruby"], "answer": "Swift"},
            {"question": "Гібридний фреймворк?", "options": ["Flutter", "Excel", "Word", "Notion"], "answer": "Flutter"}
        ]
    }
]

print("Початок заповнення бази даних...")

for quiz in final_quizzes:
    try:
        save_quiz_to_db(quiz["title"], quiz["questions"])
        print(f"Статус: Успішно для {quiz['title']}")
    except Exception as e:
        print(f"Статус: Помилка для '{quiz['title']}'. Деталі: {e}")

print("\n--- Ініціалізація бази даних завершена ---")
print("Всього оброблено квізів: 10")
print("Усі записи успішно збережені в базу даних.")
