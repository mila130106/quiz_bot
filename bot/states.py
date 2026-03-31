"""
FSM States for Quiz Bot
"""
from aiogram.fsm.state import State, StatesGroup


class QuizForm(StatesGroup):
    """States for quiz management"""
    in_progress = State()
    waiting_for_topic = State()
    waiting_for_question_count = State()
