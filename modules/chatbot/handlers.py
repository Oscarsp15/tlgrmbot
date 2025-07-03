# modules/chatbot/handlers.py
from aiogram import Router, types
from aiogram.filters import Command

from keyboards.menu import get_main_menu
from utils.language import translate_for_user

router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    """Send a welcome message and show the main menu."""
    text = f"¡Hola, {message.from_user.first_name}! 👋 Bienvenido al bot."
    await message.answer(
        await translate_for_user(text, message.from_user.id),
        reply_markup=get_main_menu(),
    )


@router.message(Command("help"))
async def send_help(message: types.Message):
    """Show help information about available commands."""
    text = (
        "Comandos disponibles:\n"
        "/start - Iniciar conversación con el bot\n"
        "/help - Mostrar este mensaje de ayuda\n"
        "/guess - Comenzar el juego de adivinar el número\n"
        "/flag - Comenzar el juego de adivinar la bandera\n"
        "/cancel - Cancelar el juego actual\n"
        "/language - Cambiar idioma"
    )
    await message.answer(await translate_for_user(text, message.from_user.id))


@router.message(Command("menu"))
async def send_menu(message: types.Message):
    """Display the bot main menu."""
    await message.answer(
        await translate_for_user("Selecciona una opción:", message.from_user.id),
        reply_markup=get_main_menu(),
    )
