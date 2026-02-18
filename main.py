import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from ai_service import generate_quiz_ai
from db_operations import (
    save_quiz_to_db, get_all_quizzes, 
    get_quiz_questions, get_question_options, check_answer
)

TOKEN = "8382165339:AAGodG-EN4v189I7VdUiMxAf_33omXGe59w"
ADMIN_ID = 623860141

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage()) 

class QuizForm(StatesGroup):
    in_progress = State()      
    waiting_for_topic = State() 

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/list")],
            [KeyboardButton(text="/new_quiz")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"), StateFilter("*"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "System initialized. Use the menu to manage quizzes.",
        reply_markup=get_main_menu()
    )

@dp.message(F.text.in_({"/list", "list", "🔙 Main Menu"}), StateFilter("*"))
@dp.message(Command("list"), StateFilter("*"))
async def cmd_list(message: Message, state: FSMContext):
    await state.clear()
    quizzes = get_all_quizzes()
    if not quizzes:
        await message.answer("Database empty. Use /new_quiz to generate content.", reply_markup=get_main_menu())
        return
    
    response = "📋 **Available Quizzes:**\n\n"
    for q_id, title in quizzes:
        response += f"ID: {q_id} | Topic: {title}\n"
    
    response += "\nSelect ID to begin testing."
    await message.answer(response, reply_markup=get_main_menu())

@dp.message(F.text.isdigit(), StateFilter(None))
async def start_quiz(message: Message, state: FSMContext):
    quiz_id = int(message.text)
    questions = get_quiz_questions(quiz_id)
    if not questions:
        await message.answer("Error: Invalid ID or empty quiz.")
        return
    await state.set_state(QuizForm.in_progress)
    await state.update_data(questions=questions, q_idx=0, score=0)
    await send_next_question(message, state)

async def send_next_question(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = data.get('questions', [])
    idx = data.get('q_idx', 0)

    if idx >= len(questions):
        final_score = data.get('score', 0)
        final_kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="/list"), KeyboardButton(text="/new_quiz")],
                [KeyboardButton(text="🔙 Main Menu")]
            ],
            resize_keyboard=True
        )
        await message.answer(
            f"🏁 **Session Summary**\nScore: {final_score} / {len(questions)}\nProcessing complete.",
            reply_markup=final_kb
        )
        await state.clear()
        return

    q_id, q_text = questions[idx]
    options = get_question_options(q_id)
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=opt[0])] for opt in options], resize_keyboard=True)
    await message.answer(f"Question {idx+1}: {q_text}", reply_markup=kb)

@dp.message(QuizForm.in_progress)
async def process_quiz_answer(message: Message, state: FSMContext):
    if message.text in ["/list", "/new_quiz", "🔙 Main Menu"]:
        await state.clear()
        return

    data = await state.get_data()
    questions = data.get('questions', [])
    idx = data.get('q_idx', 0)
    score = data.get('score', 0)
    
    q_id = questions[idx][0]
    is_correct = check_answer(q_id, message.text)
    
    if is_correct:
        await message.answer("Result: Correct answer.")
        score += 1
    else:
        await message.answer("Result: Incorrect answer.")

    await state.update_data(q_idx=idx + 1, score=score)
    await send_next_question(message, state)

@dp.message(Command("new_quiz"), StateFilter("*"))
async def start_ai_gen(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.clear()
        await message.answer("Input required topic for AI generation:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(QuizForm.waiting_for_topic)

@dp.message(QuizForm.waiting_for_topic)
async def handle_topic(message: Message, state: FSMContext):
    topic = message.text
    msg = await message.answer(f"Requesting data for: {topic}...")
    
    quiz_data = await generate_quiz_ai(topic)
    if quiz_data:
        save_quiz_to_db(topic, quiz_data)
        await msg.edit_text(f"Status: Content for '{topic}' saved. Access via /list.")
    else:
        await msg.edit_text("Error: AI service unavailable.")
    
    await state.clear()
    await message.answer("Returning to control menu.", reply_markup=get_main_menu())

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())