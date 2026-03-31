"""
Admin command handlers for Quiz Bot
Handles administrative commands
"""
import logging
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_main_menu, get_remove_keyboard, get_question_count_keyboard
from bot.states import QuizForm
from bot.utils import is_admin
from services.ai_service import generate_quiz_ai
from services import (
    save_quiz_to_db, get_user_role,
    set_user_role, register_user, get_all_users, delete_quiz
)
from config import ADMIN_ID

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("new_quiz"), StateFilter("*"))
async def start_ai_gen(message: Message, state: FSMContext):
    """Handler for /new_quiz command - starts AI quiz generation"""
    if message.from_user and is_admin(message.from_user.id):
        logger.info("Admin %s started new quiz generation flow", message.from_user.id)
        await state.clear()
        await message.answer("Введіть тему для генерації квізу за допомогою AI:", reply_markup=get_remove_keyboard())
        await state.set_state(QuizForm.waiting_for_topic)
    else:
        logger.warning("Unauthorized /new_quiz attempt by %s", message.from_user.id if message.from_user else "unknown")
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")


@router.message(QuizForm.waiting_for_topic)
async def handle_topic(message: Message, state: FSMContext):
    """Handler for receiving topic — saves it and asks for question count"""
    topic = message.text
    if not topic or not topic.strip():
        await message.answer("Будь ласка, введіть тему квізу.")
        return
    logger.info("Admin %s entered topic: %s", message.from_user.id if message.from_user else "unknown", topic)
    await state.update_data(topic=topic.strip())
    await message.answer(
        f"Тема: <b>{topic.strip()}</b>\n\nОберіть кількість питань:",
        reply_markup=get_question_count_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(QuizForm.waiting_for_question_count)


@router.message(QuizForm.waiting_for_question_count)
async def handle_question_count(message: Message, state: FSMContext):
    """Handler for receiving question count and generating quiz"""
    text = (message.text or "").strip()
    if not text.isdigit() or int(text) < 1 or int(text) > 50:
        await message.answer("Будь ласка, оберіть кількість питань з клавіатури або введіть число від 1 до 50.")
        return

    count = int(text)
    data = await state.get_data()
    topic = data.get("topic", "")
    logger.info("Admin %s requested AI quiz for topic '%s' with %d questions", message.from_user.id if message.from_user else "unknown", topic, count)
    await message.answer(f"Генеруємо {count} питань для теми: {topic}...", reply_markup=get_remove_keyboard())

    quiz_data = await generate_quiz_ai(topic, count)
    if quiz_data:
        save_quiz_to_db(topic, quiz_data)
        logger.info("AI quiz saved for topic: %s (%d questions)", topic, len(quiz_data))
        await message.answer(f"Готово! Збережено {len(quiz_data)} питань для '{topic}'. Доступ через /list.")
    else:
        logger.error("AI quiz generation failed for topic: %s", topic)
        await message.answer("Помилка: AI сервіс недоступний.")

    await state.clear()
    user_is_admin = is_admin(message.from_user.id) if message.from_user else False
    await message.answer("Повертаємося до головного меню.", reply_markup=get_main_menu(user_is_admin))


@router.message(Command("add_admin"))
async def cmd_add_admin(message: Message):
    """Handler for /add_admin command - promotes user to admin"""
    if not message.from_user or not is_admin(message.from_user.id):
        logger.warning("Unauthorized /add_admin attempt by %s", message.from_user.id if message.from_user else "unknown")
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    if not message.text:
        await message.answer("Використання: /add_admin [user_id]\nПриклад: /add_admin 123456789")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Використання: /add_admin [user_id]\nПриклад: /add_admin 123456789")
        return

    target_user_id = int(parts[1])

    # Register user if not exists
    if get_user_role(target_user_id) is None:
        register_user(target_user_id, 'admin')
        logger.info("Admin %s registered new admin %s", message.from_user.id, target_user_id)
        await message.answer(f"Користувач {target_user_id} зареєстрований як адміністратор.")
    else:
        if set_user_role(target_user_id, 'admin'):
            logger.info("Admin %s promoted user %s to admin", message.from_user.id, target_user_id)
            await message.answer(f"Користувач {target_user_id} підвищений до адміністратора.")
        else:
            logger.error("Admin %s failed to promote user %s", message.from_user.id, target_user_id)
            await message.answer(f"Помилка: Не вдалося оновити користувача {target_user_id}.")


@router.message(Command("remove_admin"))
async def cmd_remove_admin(message: Message):
    """Handler for /remove_admin command - demotes admin to user"""
    if not message.from_user or not is_admin(message.from_user.id):
        logger.warning("Unauthorized /remove_admin attempt by %s", message.from_user.id if message.from_user else "unknown")
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    if not message.text:
        await message.answer("Використання: /remove_admin [user_id]\nПриклад: /remove_admin 123456789")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Використання: /remove_admin [user_id]\nПриклад: /remove_admin 123456789")
        return

    target_user_id = int(parts[1])

    # Prevent removing super-admin
    if target_user_id == ADMIN_ID:
        logger.warning("Admin %s attempted to remove super-admin %s", message.from_user.id, ADMIN_ID)
        await message.answer(f"Неможливо видалити супер-адміністратора (ID: {ADMIN_ID}).")
        return

    if set_user_role(target_user_id, 'user'):
        logger.info("Admin %s demoted user %s to user", message.from_user.id, target_user_id)
        await message.answer(f"Користувач {target_user_id} понижений до звичайного користувача.")
    else:
        logger.error("Admin %s failed to demote user %s", message.from_user.id, target_user_id)
        await message.answer(f"Помилка: Користувач {target_user_id} не знайдений.")


@router.message(Command("delete_quiz"))
async def cmd_delete_quiz(message: Message):
    """Handler for /delete_quiz command - deletes a quiz"""
    if not message.from_user or not is_admin(message.from_user.id):
        logger.warning("Unauthorized /delete_quiz attempt by %s", message.from_user.id if message.from_user else "unknown")
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    if not message.text:
        await message.answer("Використання: /delete_quiz [quiz_id]\nПриклад: /delete_quiz 5")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Використання: /delete_quiz [quiz_id]\nПриклад: /delete_quiz 5")
        return

    quiz_id = int(parts[1])
    try:
        delete_quiz(quiz_id)
        logger.info("Admin %s deleted quiz %s", message.from_user.id, quiz_id)
        await message.answer(f"Квіз {quiz_id} успішно видалений.")
    except Exception as e:
        logger.exception("Admin %s failed to delete quiz %s", message.from_user.id, quiz_id)
        await message.answer(f"Помилка видалення квізу: {e}")


@router.message(Command("users"))
async def cmd_users(message: Message):
    """Handler for /users command - shows all registered users"""
    if not message.from_user or not is_admin(message.from_user.id):
        logger.warning("Unauthorized /users attempt by %s", message.from_user.id if message.from_user else "unknown")
        await message.answer("Доступ заборонено. Необхідні права адміністратора.")
        return

    logger.info("Admin %s requested users list", message.from_user.id)
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
