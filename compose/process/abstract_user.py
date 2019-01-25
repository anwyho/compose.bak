import json  # noqa
import logging

from abc import (ABC, abstractmethod)
from typing import (Optional)

from compose.utils.requests import (get)
from compose.utils.urls import (MESSENGER_USER_API)


def get_default_locale():
    from bot.phrasing import (DEFAULT_LOCALE)
    return DEFAULT_LOCALE


class AbstractUser(ABC):
    def __init__(self, id=None):
        self._id: str = id
        self._fn: Optional[str] = None
        self._ln: Optional[str] = None
        self._locale: Optional[str] = None

    @abstractmethod
    def retrieve_session_data(self):
        pass

    @property
    def fn(self) -> Optional[str]:
        if self._fn is None:
            self._fill_fields('first_name', 'last_name')
        return self._fn

    @property
    def ln(self) -> Optional[str]:
        if self._ln is None:
            self._fill_fields('first_name', 'last_name')
        return self._ln

    @property
    def locale(self) -> Optional[str]:
        if self._locale is None:
            self._fill_fields('locale')
        return self._locale

    def _fill_fields(self, *fields: str) -> bool:
        if self._id is None:
            return False

        logging.info(f"Getting {fields} for id {self._id}")
        queries: dict = {'fields': list(fields)}

        ok, data = get(MESSENGER_USER_API.format(fbId=self._id), json=queries)

        if not ok:
            logging.warning(f"Failed to retrieve {fields} for id {self._id}")
            return False

        self._locale = data['locale'] if 'locale' in fields and \
            'locale' in data else get_default_locale()
        if 'first_name' in fields and 'first_name' in data:
            self._fn = data['first_name']
        if 'last_name' in fields and 'last_name' in data:
            self._fn = data['last_name']

        return ok
