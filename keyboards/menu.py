from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu() -> ReplyKeyboardMarkup:
    """Return a keyboard with main bot commands."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="/help")
    builder.button(text="/guess")
    builder.button(text="/cancel")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
