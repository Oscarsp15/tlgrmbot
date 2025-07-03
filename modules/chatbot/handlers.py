# modules/chatbot/handlers.py

from aiogram import types, Dispatcher

def register_hello_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
        await message.answer(
            f"¡Hola, {message.from_user.first_name}! 👋 Bienvenido al bot."
        )

    @dp.message_handler()
    async def echo_message(message: types.Message):
        await message.answer(
            f"Has dicho: {message.text}"
        )
