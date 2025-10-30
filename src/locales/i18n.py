import logging

from functools import lru_cache


_LOG = logging.getLogger("woman-tg-bot")

LANGUAGES = {
    "ru": "src.locales.texts_ru",
    "en": "src.locales.texts_en",
    "de": "src.locales.texts_de",
    "fr": "src.locales.texts_fr",
    "it": "src.locales.texts_it",
    "es": "src.locales.texts_es",
    "pt": "src.locales.texts_pt",
    "pl": "src.locales.texts_pl",
    "hu": "src.locales.texts_hu",
    "ro": "src.locales.texts_ro",
    "fi": "src.locales.texts_fi",
    "sv": "src.locales.texts_sv",
    "tr": "src.locales.texts_tr",
    "ko": "src.locales.texts_ko",
    "ja": "src.locales.texts_ja",
    "zh": "src.locales.texts_zh",
    "hi": "src.locales.texts_hi",
}


@lru_cache
def get_locale(
    lang_code: str,
):
    try:
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
    except Exception as e:
        _LOG.error(
            f"Ошибка при загрузке локализации для lang_code={lang_code}: {e}"
        )
        try:
            return __import__(
                LANGUAGES["ru"],
                fromlist=[
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
                ],
            )
        except Exception as inner_e:
            _LOG.critical(
                f"Критическая ошибка: невозможно загрузить fallback локализацию: {inner_e}"
            )
            raise
