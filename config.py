# config.py

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN_TELEGRAM")

# API de countries y configuración del juego de banderas
COUNTRIES_API_URL = os.getenv(
    "COUNTRIES_API_URL",
    "https://restcountries.com/v3.1/all?fields=name,flags,translations",
)

FLAG_ATTEMPTS = int(os.getenv("FLAG_ATTEMPTS", "5"))
