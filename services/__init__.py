"""Services package"""
from .database import init_db
from .db_operations import (
    save_quiz_to_db,
    get_all_quizzes,
    get_quiz_questions,
    get_question_options,
    check_answer,
    register_user,
    get_user_role,
    set_user_role,
    get_all_users,
    delete_quiz
)
from .ai_service import generate_quiz_ai

__all__ = [
    'init_db',
    'save_quiz_to_db',
    'get_all_quizzes',
    'get_quiz_questions',
    'get_question_options',
    'check_answer',
    'register_user',
    'get_user_role',
    'set_user_role',
    'get_all_users',
    'delete_quiz',
    'generate_quiz_ai'
]
