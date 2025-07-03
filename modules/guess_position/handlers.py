from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from .services import generate_secret
import asyncio
from utils.language import translate_for_user

router = Router()

class Game(StatesGroup):
    playing = State()

@router.message(Command("guess"))
async def cmd_guess(msg, state: FSMContext):
    secret = generate_secret()
    await state.set_state(Game.playing)
    await state.update_data(
        secret=secret, attempts=0, history=[], 
        bot_msg_id=None, chat_id=msg.chat.id
    )
    sent = await msg.answer(
        await translate_for_user(
            "🎯 Juego iniciado: adivina el número de 6 dígitos.\nUsa /cancel para abortar.",
            msg.from_user.id,
        )
    )
    await state.update_data(bot_msg_id=sent.message_id)
    await asyncio.sleep(1)
    await msg.delete()

@router.message(Game.playing, F.text.regexp(r"^\d{6}$"))
async def process_guess(msg, state: FSMContext):
    data = await state.get_data()
    secret = data["secret"]
    guess = msg.text
    attempts = data["attempts"] + 1

    fb = [None] * 6
    secret_list = list(secret)
    for i, g in enumerate(guess):
        if g == secret[i]:
            fb[i] = "🟩"
            secret_list[i] = None
    for i, g in enumerate(guess):
        if fb[i] is None:
            if g in secret_list:
                fb[i] = "🟨"
                secret_list[secret_list.index(g)] = None
            else:
                fb[i] = "⬜"

    history = data["history"] + [("".join(fb), ''.join(guess))]
    await state.update_data(attempts=attempts, history=history)

    text = ""
    for emo, nums in history:
        spaced = "__".join(nums)
        text += f"{emo}\n{spaced}\n"
    text += await translate_for_user(
        f"Intentos: {attempts}/8.\nUsa /cancel para abortar.",
        msg.from_user.id,
    )

    # Editar mensaje del bot y eliminar usuario tras 2s
    bot = msg.bot
    temp_msg = await bot.edit_message_text(chat_id=data["chat_id"], message_id=data["bot_msg_id"], text=text)
    await asyncio.sleep(2)
    await msg.delete()

    # Victoria o derrota
    win = all(c == "🟩" for c in fb)
    if win or attempts >= 8:
        result = await translate_for_user(
            "🏆 \u00a1Ganaste!" if win else f"❌ Fin del juego. Secreto: {secret}",
            msg.from_user.id,
        )
        final_msg = await bot.edit_message_text(
            chat_id=data["chat_id"],
            message_id=data["bot_msg_id"],
            text=text + "\n" + result
        )
        await asyncio.sleep(5)
        await bot.delete_message(chat_id=data["chat_id"], message_id=final_msg.message_id)
        await state.clear()

@router.message(Command("cancel"), Game.playing)
async def cancel(msg, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    bot_msg_id = data["bot_msg_id"]
    bot = msg.bot

    # Borra historia del bot
    await bot.delete_message(chat_id=chat_id, message_id=bot_msg_id)
    temp = await msg.answer(
        await translate_for_user("🛑 Juego cancelado.", msg.from_user.id)
    )
    await asyncio.sleep(2)
    await msg.delete()
    await asyncio.sleep(5)
    await temp.delete()
    await state.clear()

@router.message(Game.playing)
async def invalid(msg, state: FSMContext):
    temp = await msg.answer(
        await translate_for_user("❗ Solo números de 6 dígitos son válidos.", msg.from_user.id)
    )
    await asyncio.sleep(1)
    await msg.delete()
    await asyncio.sleep(2)
    await temp.delete()
