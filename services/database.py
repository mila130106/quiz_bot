import sqlite3

def init_db():
    conn = sqlite3.connect('quiz_system.db')
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, role TEXT DEFAULT "user")')
    
    cursor.execute('CREATE TABLE IF NOT EXISTS quizzes (quiz_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions 
                      (question_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       quiz_id INTEGER, question_text TEXT,
                       FOREIGN KEY (quiz_id) REFERENCES quizzes (quiz_id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS options 
                      (option_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       question_id INTEGER, option_text TEXT, is_correct BOOLEAN,
                       FOREIGN KEY (question_id) REFERENCES questions (question_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_results 
                      (user_id INTEGER, quiz_id INTEGER, score INTEGER, 
                       PRIMARY KEY (user_id, quiz_id))''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database successfully initialized!")