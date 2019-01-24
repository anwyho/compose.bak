
import json
import logging

from abc import (ABC, abstractmethod)
from typing import (Optional, Tuple)

from compose.utils.requests import (get)


def get_wit_header_and_url() -> Tuple[dict, str]:
    from bot.utils.urls import (WIT_HEADER, WIT_MESSAGE_API)
    return (WIT_HEADER, WIT_MESSAGE_API)


class WitParsingError(Exception):
    pass


class AbstractWitParser(ABC):
    MIN_CONFIDENCE = 0.9

    def __init__(self, text: str, senderId: Optional[str] = None):
        self.text: str = text
        self.senderId: Optional[str] = senderId
        self.entities = self.get_entities()
        self.parse_entities()

    def get_entities(self):
        wit_header, wit_message_api = get_wit_header_and_url()
        data: dict = {}
        data['q'] = self.text[:280]  # Wit has a 280 char limit
        data['n'] = 4  # Get 4 best entities
        data['verbose'] = True
        if self.senderId:
            data['context'] = {'session_id': self.senderId}

        ok, witResp = get(url=wit_message_api, params=data, headers=wit_header)

        if not ok:
            raise WitParsingError("Failed to retrieve Wit entities")
        if 'entities' not in witResp:
            raise WitParsingError("Unexpected structure from Wit response.")

        logging.info("Successfully called Wit API")
        logging.debug(f"Wit entities: {json.dumps(witResp,indent=2)}")
        return witResp['entities']

    @abstractmethod
    def parse_entities(self):
        pass
