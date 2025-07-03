import random
import aiohttp
from config import COUNTRIES_API_URL

async def get_random_country():
    """Fetch list of countries and return random one's name and flag URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(COUNTRIES_API_URL) as resp:
            data = await resp.json()
    country = random.choice(data)
    name = country.get("translations", {}).get("spa", {}).get("common")
    if not name:
        name = country.get("name", {}).get("common", "")
    flag_url = country.get("flags", {}).get("png")
    return name, flag_url
