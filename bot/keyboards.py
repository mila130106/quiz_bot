"""
Keyboard layouts for Quiz Bot
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_main_menu(is_admin_user=False):
    """Generate main menu based on user role"""
    keyboard = [[KeyboardButton(text="/list")]]
    if is_admin_user:
        keyboard.append([KeyboardButton(text="/new_quiz")])
        keyboard.append([KeyboardButton(text="/users")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_remove_keyboard():
    """Returns a keyboard removal object"""
    return ReplyKeyboardRemove()


def get_quiz_options_keyboard(options):
    """Generate keyboard with quiz answer options"""
    keyboard = [[KeyboardButton(text=opt[0])] for opt in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
