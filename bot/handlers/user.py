"""
User command handlers for Quiz Bot
Handles commands available to all users
"""
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_main_menu, get_quiz_options_keyboard
from bot.states import QuizForm
from bot.utils import is_admin
from services import (
    register_user, get_user_role, get_all_quizzes,
    get_quiz_questions, get_question_options, check_answer
)
from config import ADMIN_ID

router = Router()


@router.message(Command("start"), StateFilter("*"))
async def cmd_start(message: Message, state: FSMContext):
    """Handler for /start command - registers user and shows main menu"""
    await state.clear()
    user_id = message.from_user.id

    # Auto-register user if not in DB
    if get_user_role(user_id) is None:
        # Assign admin role if this is the super-admin from .env
        role = 'admin' if user_id == ADMIN_ID else 'user'
        register_user(user_id, role)

    user_is_admin = is_admin(user_id)
    await message.answer(
        "Систему ініціалізовано. Використовуйте меню для керування квізами.",
        reply_markup=get_main_menu(user_is_admin)
    )


@router.message(F.text.in_({"/list", "list", "🔙 Головне меню"}), StateFilter("*"))
@router.message(Command("list"), StateFilter("*"))
async def cmd_list(message: Message, state: FSMContext):
    """Handler for /list command - shows available quizzes"""
    await state.clear()
    user_is_admin = is_admin(message.from_user.id)
    quizzes = get_all_quizzes()
    if not quizzes:
        await message.answer("База даних порожня. Використовуйте /new_quiz для створення контенту.", reply_markup=get_main_menu(user_is_admin))
        return

    response = "📋 **Доступні квізи:**\n\n"
    for q_id, title in quizzes:
        response += f"ID: {q_id} | Тема: {title}\n"

    response += "\nВведіть ID для початку тестування."
    await message.answer(response, reply_markup=get_main_menu(user_is_admin))


@router.message(F.text.isdigit(), StateFilter(None))
async def start_quiz(message: Message, state: FSMContext):
    """Handler for starting a quiz by ID"""
    quiz_id = int(message.text)
    questions = get_quiz_questions(quiz_id)
    if not questions:
        await message.answer("Помилка: невірний ID або порожній квіз.")
        return
    await state.set_state(QuizForm.in_progress)
    await state.update_data(questions=questions, q_idx=0, score=0)
    await send_next_question(message, state)


async def send_next_question(message: Message, state: FSMContext):
    """Send next question or show final results"""
    data = await state.get_data()
    questions = data.get('questions', [])
    idx = data.get('q_idx', 0)

    if idx >= len(questions):
        final_score = data.get('score', 0)
        user_is_admin = is_admin(message.from_user.id)
        await message.answer(
            f"🏁 **Підсумок тестування**\nБали: {final_score} / {len(questions)}\nТестування завершено.",
            reply_markup=get_main_menu(user_is_admin)
        )
        await state.clear()
        return

    q_id, q_text = questions[idx]
    options = get_question_options(q_id)
    kb = get_quiz_options_keyboard(options)
    await message.answer(f"Питання {idx+1}: {q_text}", reply_markup=kb)


@router.message(QuizForm.in_progress)
async def process_quiz_answer(message: Message, state: FSMContext):
    """Handler for quiz answer processing"""
    if message.text in ["/list", "/new_quiz", "🔙 Головне меню"]:
        await state.clear()
        return

    data = await state.get_data()
    questions = data.get('questions', [])
    idx = data.get('q_idx', 0)
    score = data.get('score', 0)

    q_id = questions[idx][0]
    is_correct = check_answer(q_id, message.text)

    if is_correct:
        await message.answer("Результат: Правильна відповідь.")
        score += 1
    else:
        await message.answer("Результат: Неправильна відповідь.")

    await state.update_data(q_idx=idx + 1, score=score)
    await send_next_question(message, state)
