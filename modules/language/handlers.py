from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.language import SUPPORTED_LANGS, set_user_language, translate_for_user

router = Router()


@router.message(Command("language"))
async def choose_language(message: types.Message):
    builder = InlineKeyboardBuilder()
    for code, label in SUPPORTED_LANGS.items():
        builder.button(text=label, callback_data=f"setlang:{code}")
    await message.answer(
        await translate_for_user("Selecciona un idioma:", message.from_user.id),
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data.startswith("setlang:"))
async def set_lang(callback: types.CallbackQuery):
    code = callback.data.split(":", 1)[1]
    set_user_language(callback.from_user.id, code)
    await callback.message.edit_text(
        await translate_for_user("Idioma actualizado.", callback.from_user.id)
    )
    await callback.answer()
