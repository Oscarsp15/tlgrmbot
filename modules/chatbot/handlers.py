# modules/chatbot/handlers.py
from aiogram import Router, types
from aiogram.filters import Command  # filtro para comandos

router = Router()

@router.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    await message.answer(f"¡Hola, {message.from_user.first_name}! 👋 Bienvenido al bot.")

'''@router.message()
async def echo(message: types.Message):
    await message.answer(f"Has dicho: {message.text}")''' #repite lo que el usuario dice

def register_hello_handlers(dp):
    dp.include_router(router)
