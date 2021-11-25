import six
from google.cloud import translate_v2 as translate
from google.cloud.exceptions import BadRequest
from loguru import logger

from lib.translators.exceptions import TranslationException


def translate_text(text: str, target_lang: str, source_lang: str = None):
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    try:
        result = translate_client.translate(
            text, target_language=target_lang, source_language=source_lang
        )
        return result.get("translatedText", text)
    except BadRequest as e:
        logger.error('Google translate error:{error}', error=str(e))
        raise TranslationException("Wrong input or google-translate error")
