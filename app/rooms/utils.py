from loguru import logger

from app.users.constants import Lang
from lib.translators.exceptions import TranslationException
from lib.translators import translate_text


def translate(text: str, from_lang: Lang, to_lang: Lang) -> str:
    if from_lang != to_lang:
        try:
            text = translate_text(
                text=text, source_lang=from_lang.value, target_lang=to_lang.value
            )
        except TranslationException:
            logger.error("Cannot translate {l1}->{l2}", l1=from_lang, l2=to_lang)
    return text


def get_translated_messages(messages, lang: Lang):
    resp = []
    for msg in messages:
        msg.text = translate(text=msg.text, from_lang=msg.lang, to_lang=lang)
        resp.append(msg)
    return resp
