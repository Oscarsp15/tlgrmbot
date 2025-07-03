from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from utils.language import translate_for_user

from config import FLAG_ATTEMPTS
from .services import get_random_country

router = Router()

class FlagGame(StatesGroup):
    playing = State()

@router.message(Command("flag"))
async def cmd_flag(msg, state: FSMContext):
    name, flag_url = await get_random_country()
    await state.set_state(FlagGame.playing)
    await state.update_data(
        country=name,
        flag=flag_url,
        attempts=0,
        history=[],
        bot_msg_id=None,
        chat_id=msg.chat.id,
    )
    sent = await msg.answer_photo(
        flag_url,
        caption=await translate_for_user(
            "⚫️ Adivina la bandera. Usa /cancel para abortar.",
            msg.from_user.id,
        ),
    )
    await state.update_data(bot_msg_id=sent.message_id)
    await asyncio.sleep(1)
    await msg.delete()

@router.message(FlagGame.playing, F.text)
async def process_guess(msg, state: FSMContext):
    data = await state.get_data()
    guess = msg.text.strip()
    attempts = data["attempts"] + 1
    history = data["history"] + [f"{guess} - {'✅' if guess.lower()==data['country'].lower() else '❌'}"]
    await state.update_data(attempts=attempts, history=history)

    caption = "\n".join(
        [
            await translate_for_user("⚫️ Adivina la bandera:", msg.from_user.id),
            *history,
            await translate_for_user(
                f"Intentos: {attempts}/{FLAG_ATTEMPTS}.", msg.from_user.id
            ),
            await translate_for_user("Usa /cancel para abortar.", msg.from_user.id),
        ]
    )
    bot = msg.bot
    await bot.edit_message_caption(chat_id=data["chat_id"], message_id=data["bot_msg_id"], caption=caption)
    await asyncio.sleep(2)
    await msg.delete()

    win = guess.lower() == data["country"].lower()
    if win or attempts >= FLAG_ATTEMPTS:
        result = await translate_for_user(
            "🏆 \u00a1Correcto!" if win else f"❌ Fin del juego. Era {data['country']}",
            msg.from_user.id,
        )
        final_caption = caption + "\n" + result
        final_msg = await bot.edit_message_caption(chat_id=data["chat_id"], message_id=data["bot_msg_id"], caption=final_caption)
        await asyncio.sleep(5)
        await bot.delete_message(chat_id=data["chat_id"], message_id=final_msg.message_id)
        await state.clear()

@router.message(Command("cancel"), FlagGame.playing)
async def cancel(msg, state: FSMContext):
    data = await state.get_data()
    bot = msg.bot
    await bot.delete_message(chat_id=data["chat_id"], message_id=data["bot_msg_id"])
    temp = await msg.answer(
        await translate_for_user("🔚 Juego cancelado.", msg.from_user.id)
    )
    await asyncio.sleep(2)
    await msg.delete()
    await asyncio.sleep(5)
    await temp.delete()
    await state.clear()

@router.message(FlagGame.playing)
async def invalid(msg, state: FSMContext):
    temp = await msg.answer(
        await translate_for_user("❗ Ingresa el nombre de un país.", msg.from_user.id)
    )
    await asyncio.sleep(1)
    await msg.delete()
    await asyncio.sleep(2)
    await temp.delete()
