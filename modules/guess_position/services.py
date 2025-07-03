# modules/guess_position/services.py

import random

def generate_secret() -> str:
    """Genera un número secreto de 6 dígitos."""
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

def evaluate_guess(secret: str, guess: str) -> int:
    """Cuenta cuántos dígitos están en la posición correcta."""
    return sum(1 for s, g in zip(secret, guess) if s == g)
