import requests

from app.config import LIBRE_TRANSLATE_API_KEY
from lib.translators.exceptions import TranslationException


def translate_text(text: str, target_lang: str, source_lang: str):
    resp = requests.post(
        "https://libretranslate.de/translate",
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
    raise TranslationException("Wrong input or libre-translate error")
