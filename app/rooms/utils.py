from app.users.constants import Lang


def translate(text: str, from_lang: Lang, to_lang: Lang) -> str:
    # TODO: call external translation API
    if from_lang != to_lang:
        return f"Translated {from_lang}->{to_lang}: {text}"
    return text


def get_translated_messages(messages, lang: Lang):
    resp = []
    for msg in messages:
        msg.text = translate(text=msg.text, from_lang=msg.lang, to_lang=lang)
        resp.append(msg)
    return resp
