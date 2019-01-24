import logging
import random as r
import time

from types import ModuleType
from typing import (List, Tuple, Optional)  # noqa: F401

from .locales import (DEFAULT_LOCALE, import_locale_module)

USE_GLOBAL_DICT = True


class Phrase:

    ATTR_PREFIX = '_attr_'

    def __init__(self, initialLocale=None):
        self._phraseModule: ModuleType = None
        self._phrases: List[str] = []
        self._locale: str = initialLocale
        self._set_locale(self._locale)
        self._attributes: dict = {}
        if USE_GLOBAL_DICT:
            globalDictName = 'phrases_' + self._locale
            if not hasattr(globals(), globalDictName):
                globals()[globalDictName] = {}
            self._attributes = globals()[globalDictName]

    def __str__(self) -> str:
        return self.build()

    def flush(self) -> None:
        self._phrases.clear()
        self.sentence = ''

    def build(self) -> str:
        self.sentence = ' '.join(self._phrases)
        self._phrases.clear()
        return self.sentence

    def get(self,
            phraseType: str,
            customText: bool = False,
            **phraseArgs):
        """Get a type of phrase"""
        if customText:
            self._phrases.append(phraseType)
            return self

        # Get phrases from cache or database
        phrase = self._r_choice(
            *self.findPhrases(phraseType, **phraseArgs)
            # Format gotten phrase with own attributes
        ).format(**self._attributes)

        if phrase:
            self._phrases.append(phrase)

        return self

    def findPhrases(
            self,
            phraseType: str,
            useName: bool = False) -> List[List[str]]:
        timeOfDay, timeOfDayNoNight = get_time_of_day(
            phraseModule=self._phraseModule)

        self.add_attributes(
            timeOfDay=timeOfDay,
            timeOfDayNoNight=timeOfDayNoNight)

        # HACK: Not abstracted enough
        return (
            self._get_or_load_phrases(phraseType),
            self._get_or_load_phrases(
                (phraseType + 'WName')) if useName else []
        )

    def _get_or_load_phrases(self, phraseType: str) -> list:
        # NOTE: The global variables are used because they can be preserved from one lambda call to the next  # noqa: E501
        keyName = self.ATTR_PREFIX + phraseType
        res = self._attributes.get(keyName, [])
        if res == []:
            self.add_attributes(
                **{keyName: getattr(self._phraseModule, phraseType, [])})
            res = self._attributes.get(keyName, [])
        return res

    def get_attribute(self, phraseType: Optional[str] = None):
        return self._attributes.get(phraseType, []) \
            if phraseType else self._attributes

    def add_attributes(self, **nameToVal) -> None:
        self._attributes = {**self._attributes, **nameToVal}

    def _r_choice(self, *lists: List[str]):
        try:
            return r.choice(r.choices(lists, weights=map(len, lists))[0])
        except IndexError:
            return ''

    @property
    def locale(self) -> str:
        return self._locale

    @locale.setter
    def locale(self, newLocale: Optional[str]) -> None:
        self._set_locale(newLocale)

    def _set_locale(self, newLocale: Optional[str] = None) \
            -> Tuple[ModuleType, str]:
        """
        Idempotent function that sets locale for Phrase class. If no
            locale is given, self._locale is set and returned with
            fallback to default locale.
        Always returns a usable phrases module or raises an error.
        """

        localePkg = None
        if newLocale is None:  # No argument given
            if self._locale is None:  # No locale set
                # Then set default locale
                localePkg = self._set_locale(DEFAULT_LOCALE)
            else:  # Locale set
                # Then set locale to import phrase module
                localePkg = self._set_locale(self._locale)
        # Locale is set and phrase module exists
        elif newLocale == self._locale and \
                self._phraseModule is not None:
            # Then return current phrase module
            localePkg = (self._phraseModule, self._locale)

        else:  # Locale is set but phrase module is None
            # Then import a new phrase module
            self._phraseModule, self._locale = \
                Phrase.safe_locale_import(newLocale)
            localePkg = (self._phraseModule, self._locale)
        return localePkg

    @staticmethod
    def safe_locale_import(newLocale: str) -> Tuple[ModuleType, str]:
        """Tries to import a locale with default locale as backup"""
        newLocale = newLocale.lower() if isinstance(newLocale, str) \
            else DEFAULT_LOCALE

        try:
            localeImport = import_locale_module(newLocale)
        except (ImportError, KeyError) as e:
            # Sets default locale as fallback
            localeImport = import_locale_module()
            logging.warning(
                f"Failed to import package for locale {newLocale}. Error: {e}")
            print(
                f"Failed to import package for locale {newLocale}. Error: {e}")
        finally:
            return localeImport


def get_time_of_day(phraseModule) -> Tuple[str, str]:
    """Figure out the time of day and return it and a no-night alternative."""
    timeOfDay = getattr(phraseModule, 'timeOfDay', {})
    hour = time.localtime().tm_hour

    result = (timeOfDay['night'], timeOfDay['generic'])
    if 21 < hour or hour <= 4:
        result = (timeOfDay['night'], timeOfDay['generic'])
    elif 16 < hour:
        result = (timeOfDay['evening'], timeOfDay['evening'])
    elif 11 < hour:
        result = (timeOfDay['afternoon'], timeOfDay['afternoon'])
    elif 4 < hour:
        if r.randint(0, 3) != 0:
            result = (timeOfDay['morning'], timeOfDay['morning'])
        else:
            result = (timeOfDay['generic'], timeOfDay['generic'])
    return result
