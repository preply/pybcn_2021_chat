import requests
from loguru import logger

from app.config import LIBRE_TRANSLATE_API_KEY
from lib.translators.exceptions import TranslationException

API_URL = "https://libretranslate.de"

def translate_text(text: str, target_lang: str, source_lang: str):
    resp = requests.post(
        f"{API_URL}/translate",
        data={
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "api_key": LIBRE_TRANSLATE_API_KEY,
        },
    )
    if resp.status_code == 200:
        data = resp.json()
        return data.get("translatedText", text)
    else:
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            logger.error(e)
            raise TranslationException('Libre Translate failed') from e
