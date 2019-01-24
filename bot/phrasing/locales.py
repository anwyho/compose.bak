"""
The locales module keeps a list of all supported locales and returns
    errors on import failures.
"""

import importlib
import logging
import os

from types import ModuleType
from typing import (Tuple, Optional)  # noqa: F401

from .supported_locales import (DEFAULT_LOCALE, SUPPORTED_LOCALES)

PROJECT_NAME = 'bartbot'
PHRASES_MODULE = 'bot.phrasing.phrases'


def import_locale_module(locale: str = DEFAULT_LOCALE) \
        -> Tuple[ModuleType, str]:
    """
    Import a locale-specific module of given locale in bot.phrasing.*
    """
    locale = locale.lower()
    if locale in SUPPORTED_LOCALES:
        logging.info(f"Importing locale {locale}")
        localePkg = importlib.import_module(
            f".{PROJECT_NAME}_{SUPPORTED_LOCALES[locale]}",
            package=PHRASES_MODULE)

        return localePkg, locale

    else:
        if locale == DEFAULT_LOCALE:
            logging.error(f"Couldn't find default locale. Probably unset it or dereferenced it in `{os.getcwd()}/bot/phrasing/locales.py. Fix ASAP!")  # noqa: E501
            raise ModuleNotFoundError("Support for default locale is not implemented. Make sure the default locale is set or implemented.")  # noqa: E501
        else:
            raise KeyError(f"Locale {locale} is not in list of supported locales")  # noqa: E501
