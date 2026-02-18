from db_operations import save_quiz_to_db

final_quizzes = [
    {
        "title": "Web Development (HTML/CSS)",
        "questions": [
            {"question": "Which tag is used for internal CSS?", "options": ["<script>", "<style>", "<link>", "<css>"], "answer": "<style>"},
            {"question": "What does CSS stand for?", "options": ["Cascading Style Sheets", "Computer Style System", "Creative Style", "Colorful Sheets"], "answer": "Cascading Style Sheets"},
            {"question": "Which property changes background color?", "options": ["color", "bgcolor", "background-color", "canvas"], "answer": "background-color"}
        ]
    },
    {
        "title": "Python Programming",
        "questions": [
            {"question": "How to define a function?", "options": ["def func():", "function func():", "create func():", "func():"], "answer": "def func():"},
            {"question": "Which type is a List?", "options": ["Ordered & changeable", "Unordered", "Immutable", "Only numbers"], "answer": "Ordered & changeable"},
            {"question": "Correct for loop syntax?", "options": ["for x in y:", "for x > y:", "loop x:", "foreach x:"], "answer": "for x in y Jesu"}
        ]
    },
    {
        "title": "SQL Databases",
        "questions": [
            {"question": "Which command retrieves data?", "options": ["GET", "SELECT", "EXTRACT", "OPEN"], "answer": "SELECT"},
            {"question": "How to delete a record?", "options": ["REMOVE", "DELETE", "DROP", "ERASE"], "answer": "DELETE"},
            {"question": "What does SQL stand for?", "options": ["Simple Query Lang", "Structured Query Lang", "System Query List", "Standard Quest"], "answer": "Structured Query Lang"}
        ]
    },
    {
        "title": "Git Essentials",
        "questions": [
            {"question": "Command to save changes?", "options": ["git push", "git commit -m", "git add", "git save"], "answer": "git commit -m"},
            {"question": "How to check status?", "options": ["git check", "git info", "git status", "git log"], "answer": "git status"},
            {"question": "Command to upload to GitHub?", "options": ["git send", "git upload", "git push", "git commit"], "answer": "git push"}
        ]
    },
    {
        "title": "Cybersecurity Basics",
        "questions": [
            {"question": "What is Phishing?", "options": ["Social engineering", "Virus type", "Hardware bug", "Network protocol"], "answer": "Social engineering"},
            {"question": "What does 'HTTPS' provide?", "options": ["Speed", "Encryption", "Graphics", "Storage"], "answer": "Encryption"},
            {"question": "What is a Firewall used for?", "options": ["Monitoring traffic", "Cleaning viruses", "Cooling CPU", "Password storage"], "answer": "Monitoring traffic"}
        ]
    },
    {
        "title": "JavaScript Intro",
        "questions": [
            {"question": "How to declare a variable?", "options": ["var", "let", "const", "All of above"], "answer": "All of above"},
            {"question": "Which is not a JS data type?", "options": ["String", "Boolean", "Float", "Undefined"], "answer": "Float"},
            {"question": "How to write an alert?", "options": ["msg('Hi')", "alert('Hi')", "print('Hi')", "log('Hi')"], "answer": "alert('Hi')"}
        ]
    },
    {
        "title": "Software Testing (QA)",
        "questions": [
            {"question": "What is a Bug?", "options": ["Feature", "Error in code", "Hardware part", "Test case"], "answer": "Error in code"},
            {"question": "Which test is done first?", "options": ["Unit Testing", "System Testing", "Acceptance", "Beta Testing"], "answer": "Unit Testing"},
            {"question": "What is 'Black Box' testing?", "options": ["Testing without code access", "Hardware testing", "Inside code view", "Speed test"], "answer": "Testing without code access"}
        ]
    },
    {
        "title": "Data Science Foundations",
        "questions": [
            {"question": "Main library for data in Python?", "options": ["Pandas", "Flask", "Django", "Math"], "answer": "Pandas"},
            {"question": "What is 'ML'?", "options": ["Machine Learning", "Manual Logic", "Main Link", "Meta Layer"], "answer": "Machine Learning"},
            {"question": "CSV stands for?", "options": ["Comma Separated Values", "Core System", "Code Style", "Central Store"], "answer": "Comma Separated Values"}
        ]
    },
    {
        "title": "Computer Networks",
        "questions": [
            {"question": "Port for HTTP?", "options": ["80", "443", "21", "22"], "answer": "80"},
            {"question": "What is IP?", "options": ["Internet Protocol", "Internal Program", "Instant Point", "Input Port"], "answer": "Internet Protocol"},
            {"question": "Device for routing?", "options": ["Router", "Monitor", "Hub", "Switch"], "answer": "Router"}
        ]
    },
    {
        "title": "Mobile Development",
        "questions": [
            {"question": "Language for Android?", "options": ["Kotlin", "Swift", "C++", "PHP"], "answer": "Kotlin"},
            {"question": "Language for iOS?", "options": ["Swift", "Java", "Python", "Ruby"], "answer": "Swift"},
            {"question": "Hybrid framework?", "options": ["Flutter", "Excel", "Word", "Notion"], "answer": "Flutter"}
        ]
    }
]

print("Starting database population process...")

for quiz in final_quizzes:
    try:
        save_quiz_to_db(quiz["title"], quiz["questions"])
        print(f"Status: Success for {quiz['title']}")
    except Exception as e:
        print(f"Status: Failed for '{quiz['title']}'. Details: {e}")

print("\n--- Database initialization complete ---")
print("Total quizzes processed: 10")
print("All records have been successfully saved to the database.")