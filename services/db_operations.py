import sqlite3

def save_quiz_to_db(title, questions_data):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quizzes (title) VALUES (?)", (title,))
    quiz_id = cursor.lastrowid
    for q in questions_data:
        cursor.execute("INSERT INTO questions (quiz_id, question_text) VALUES (?, ?)", (quiz_id, q['question']))
        q_id = cursor.lastrowid
        for opt in q['options']:
            cursor.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (?, ?, ?)",
                           (q_id, opt, 1 if opt == q['answer'] else 0))
    conn.commit()
    conn.close()

def get_all_quizzes():
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT quiz_id, title FROM quizzes")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_quiz_questions(quiz_id):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question_id, question_text FROM questions WHERE quiz_id = ? ORDER BY question_id", (quiz_id,))
    questions = cursor.fetchall()
    conn.close()
    return questions

def get_question_options(question_id):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT option_text, is_correct FROM options WHERE question_id = ?", (question_id,))
    options = cursor.fetchall()
    conn.close()
    return options

def check_answer(question_id, answer_text):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT is_correct FROM options WHERE question_id = ? AND option_text = ?", (question_id, answer_text))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# User role management functions
def register_user(user_id, role='user'):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, role) VALUES (?, ?)", (user_id, role))
    conn.commit()
    conn.close()

def get_user_role(user_id):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def set_user_role(user_id, role):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, user_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def get_all_users():
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, role FROM users ORDER BY role DESC, user_id")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_quiz(quiz_id):
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question_id FROM questions WHERE quiz_id = ?", (quiz_id,))
    question_ids = [row[0] for row in cursor.fetchall()]
    for q_id in question_ids:
        cursor.execute("DELETE FROM options WHERE question_id = ?", (q_id,))
    cursor.execute("DELETE FROM questions WHERE quiz_id = ?", (quiz_id,))
    cursor.execute("DELETE FROM quizzes WHERE quiz_id = ?", (quiz_id,))
    cursor.execute("DELETE FROM user_results WHERE quiz_id = ?", (quiz_id,))
    conn.commit()
    conn.close()