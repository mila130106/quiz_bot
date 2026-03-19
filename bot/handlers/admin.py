"""
Admin command handlers for Quiz Bot
Handles administrative commands
"""
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_main_menu, get_remove_keyboard
from bot.states import QuizForm
from bot.utils import is_admin
from services import (
    generate_quiz_ai, save_quiz_to_db, get_user_role,
    set_user_role, register_user, get_all_users, delete_quiz
)
from config import ADMIN_ID

router = Router()


@router.message(Command("new_quiz"), StateFilter("*"))
async def start_ai_gen(message: Message, state: FSMContext):
    """Handler for /new_quiz command - starts AI quiz generation"""
    if is_admin(message.from_user.id):
        await state.clear()
        await message.answer("Введіть тему для генерації квізу за допомогою AI:", reply_markup=get_remove_keyboard())
        await state.set_state(QuizForm.waiting_for_topic)
    else:
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")


@router.message(QuizForm.waiting_for_topic)
async def handle_topic(message: Message, state: FSMContext):
    """Handler for processing quiz topic and generating quiz"""
    topic = message.text
    msg = await message.answer(f"Запит даних для теми: {topic}...")

    quiz_data = await generate_quiz_ai(topic)
    if quiz_data:
        save_quiz_to_db(topic, quiz_data)
        await msg.edit_text(f"Статус: Контент для '{topic}' збережено. Доступ через /list.")
    else:
        await msg.edit_text("Помилка: AI сервіс недоступний.")

    await state.clear()
    user_is_admin = is_admin(message.from_user.id)
    await message.answer("Повертаємося до головного меню.", reply_markup=get_main_menu(user_is_admin))


@router.message(Command("add_admin"))
async def cmd_add_admin(message: Message):
    """Handler for /add_admin command - promotes user to admin"""
    if not is_admin(message.from_user.id):
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Використання: /add_admin [user_id]\nПриклад: /add_admin 123456789")
        return

    target_user_id = int(parts[1])

    # Register user if not exists
    if get_user_role(target_user_id) is None:
        register_user(target_user_id, 'admin')
        await message.answer(f"Користувач {target_user_id} зареєстрований як адміністратор.")
    else:
        if set_user_role(target_user_id, 'admin'):
            await message.answer(f"Користувач {target_user_id} підвищений до адміністратора.")
        else:
            await message.answer(f"Помилка: Не вдалося оновити користувача {target_user_id}.")


@router.message(Command("remove_admin"))
async def cmd_remove_admin(message: Message):
    """Handler for /remove_admin command - demotes admin to user"""
    if not is_admin(message.from_user.id):
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Використання: /remove_admin [user_id]\nПриклад: /remove_admin 123456789")
        return

    target_user_id = int(parts[1])

    # Prevent removing super-admin
    if target_user_id == ADMIN_ID:
        await message.answer(f"Неможливо видалити супер-адміністратора (ID: {ADMIN_ID}).")
        return

    if set_user_role(target_user_id, 'user'):
        await message.answer(f"Користувач {target_user_id} понижений до звичайного користувача.")
    else:
        await message.answer(f"Помилка: Користувач {target_user_id} не знайдений.")


@router.message(Command("delete_quiz"))
async def cmd_delete_quiz(message: Message):
    """Handler for /delete_quiz command - deletes a quiz"""
    if not is_admin(message.from_user.id):
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Використання: /delete_quiz [quiz_id]\nПриклад: /delete_quiz 5")
        return

    quiz_id = int(parts[1])
    try:
        delete_quiz(quiz_id)
        await message.answer(f"Квіз {quiz_id} успішно видалений.")
    except Exception as e:
        await message.answer(f"Помилка видалення квізу: {e}")


@router.message(Command("users"))
async def cmd_users(message: Message):
    """Handler for /users command - shows all registered users"""
    if not is_admin(message.from_user.id):
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    users = get_all_users()
    if not users:
        await message.answer("Жодного користувача ще не зареєстровано.")
        return

    response = "👥 **Зареєстровані користувачі:**\n\n"
    for user_id, role in users:
        role_icon = "👑" if role == 'admin' else "👤"
        super_mark = " (СУПЕР)" if user_id == ADMIN_ID else ""
        role_name = "АДМІН" if role == 'admin' else "КОРИСТУВАЧ"
        response += f"{role_icon} {user_id} | {role_name}{super_mark}\n"

    await message.answer(response)
