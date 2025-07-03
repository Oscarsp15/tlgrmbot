# modules/chatbot/handlers.py
from aiogram import Router, types
from aiogram.filters import Command  # filtro para comandos

from keyboards.menu import get_main_menu

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        f"¡Hola, {message.from_user.first_name}! 👋 Bienvenido al bot.",
        reply_markup=get_main_menu(),
    )


@router.message(Command("help"))
async def send_help(message: types.Message):
    """Muestra información de ayuda sobre los comandos disponibles."""
    text = (
        "Comandos disponibles:\n"
        "/start - Iniciar conversación con el bot\n"
        "/help - Mostrar este mensaje de ayuda\n"
        "/guess - Comenzar el juego de adivinar el número\n"
        "/cancel - Cancelar el juego actual"
    )
    await message.answer(text)


@router.message(Command("menu"))
async def send_menu(message: types.Message):
    """Muestra el menú principal del bot."""
    await message.answer("Selecciona una opción:", reply_markup=get_main_menu())

'''@router.message()
async def echo(message: types.Message):
    await message.answer(f"Has dicho: {message.text}")''' #repite lo que el usuario dice

def register_hello_handlers(dp):
    dp.include_router(router)
