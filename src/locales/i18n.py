from functools import lru_cache


LANGUAGES = {
    "ru": "locales.texts_ru",
    "en": "locales.texts_en",
    "de": "locales.texts_de",
    "fr": "locales.texts_fr",
    "it": "locales.texts_it",
    "es": "locales.texts_es",
    "pt": "locales.texts_pt",
    "pl": "locales.texts_pl",
    "hu": "locales.texts_hu",
    "ro": "locales.texts_ro",
    "fi": "locales.texts_fi",
    "sv": "locales.texts_sv",
    "tr": "locales.texts_tr",
    "ko": "locales.texts_ko",
    "ja": "locales.texts_ja",
    "zh": "locales.texts_zh",
    "hi": "locales.texts_hi",
}


@lru_cache
def get_locale(
    lang_code: str,
):
    if lang_code not in LANGUAGES:
        lang_code = "ru"  # дефолтный язык
    module = __import__(LANGUAGES[lang_code], fromlist=[
        "start",
        "about_us",
        "choose_girl",
        "girls",
        "girl_description_gera",
        "girl_description_eva",
        "girl_description_veronika",
        "girl_description_kate",
        "girl_name_gera",
        "girl_name_eva",
        "girl_name_veronika",
        "girl_name_kate",
        "before_buy",
        "helping",
        "subscription_month",
        "subscription_year",
        "subscription_error",
        "access_functions_in_bot",
        "subscription_activate",
        "subscription_year_activate",
        "subscription_activate_id_payment",
        "example_talk_with_bot",
        "thinking_bot",
        "kb_help",
        "kb_about",
        "kb_confirm_18",
        "kb_see_all",
        "kb_subscribtion_year",
        "kb_subscribtion",
        "error_payment",
        "decorator_confirm_18",
    ])
    return module

