import json
import asyncio
from pathlib import Path
from googletrans import Translator

DATA_FILE = Path("data/languages.json")

SUPPORTED_LANGS = {
    "es-latam": "Espa\u00f1ol LATAM",
    "es": "Espa\u00f1ol",
    "en": "English",
    "fr": "Fran\u00e7ais",
    "it": "Italiano",
    "pt": "Portugu\u00eas",
}

DEFAULT_LANG = "es"

try:
    LANG_PREFS = json.loads(DATA_FILE.read_text())
except FileNotFoundError:
    LANG_PREFS = {}


def save_prefs() -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(LANG_PREFS))


def set_user_language(user_id: int, lang: str) -> None:
    LANG_PREFS[str(user_id)] = lang
    save_prefs()


def get_user_language(user_id: int) -> str:
    return LANG_PREFS.get(str(user_id), DEFAULT_LANG)


async def translate_text(text: str, dest: str) -> str:
    dest_code = "es" if dest.startswith("es") else dest
    if dest_code == "es":
        return text
    loop = asyncio.get_running_loop()
    translator = Translator()
    return await loop.run_in_executor(
        None, lambda: translator.translate(text, dest=dest_code).text
    )


async def translate_for_user(text: str, user_id: int) -> str:
    lang = get_user_language(user_id)
    return await translate_text(text, lang)
