# Telegram Bot

Este proyecto es un bot para Telegram construido con [aiogram](https://docs.aiogram.dev/).
Incluye dos funcionalidades principales:

- **Chatbot**: Responde al comando `/start` o `/help` dando la bienvenida al usuario.
- **Guess Position**: Un juego para adivinar un número secreto de 6 dígitos. El bot indica con emojis el acierto de cada dígito y finaliza al acertar o tras 8 intentos. Se puede cancelar con `/cancel`.

## Requisitos

- Python 3.11 o superior.
- Dependencias listadas en `requirements.txt`.

## Instalación

1. Clona el repositorio y entra en la carpeta:

```bash
$ git clone <repo-url>
$ cd tlgrmbot
```

2. Crea un entorno virtual (opcional) e instala dependencias:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

3. Crea un archivo `.env` en la raíz con tu token de bot:

```
TOKEN_TELEGRAM=tu-token-aquí
```

## Uso

Ejecuta el bot con:

```bash
$ python app.py
```

El bot comenzará a hacer *polling* de mensajes. Los comandos disponibles son:

- `/start` o `/help` – Mensaje de bienvenida.
- `/guess` – Inicia el juego "Guess Position".
- `/cancel` – Cancela el juego en curso.

## Estructura del proyecto

- `app.py` – Punto de entrada del bot.
- `config.py` – Carga la variable `TOKEN_TELEGRAM` desde el entorno.
- `modules/` – Funcionalidades del bot.
  - `chatbot/` – Gestión de los mensajes de bienvenida.
  - `guess_position/` – Lógica del juego y sus manejadores.
- `requirements.txt` – Lista de dependencias de Python.

## Licencia

MIT
