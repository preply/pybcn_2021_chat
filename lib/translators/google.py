import six
from google.cloud import translate_v2 as translate
from google.cloud.exceptions import BadRequest

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
        if result and "translatedText" in result:
            return result["translatedText"]
    except BadRequest:
        pass
    raise TranslationException("Wrong input or google-translate error")
