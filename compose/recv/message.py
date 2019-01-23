
import json  # noqa
import logging  # noqa
import sys
import wrapt

from abc import (ABC, ABCMeta)
from typing import (Tuple, TypeVar)

from compose.utils.errors import (generate_error_message)

Coordinate = Tuple[float, float]
ParamType = TypeVar('ParamType', str, int, Coordinate, list)


class MessageParsingError(Exception):
    pass


@wrapt.decorator
def safe_parse(wrapped, instance, args, kwargs):
    """
    This wrapper attempts to catch and handle any errors that indicate
        that entries were incorrectly formatted, returning None if
        unable to import.
    """

    try:
        return wrapped(*args, **kwargs)
    except (AttributeError, IndexError, KeyError, TypeError) as e:
        raise MessageParsingError(f"Couldn't parse JSON entry. Error: {e}")
    except Exception as e:
        generate_error_message(sys.exec_info(), e)


class Message(ABC):  # Message is an Abstract Base Class
    SUPPORTED_MESSAGE_TYPES = ['TEXT', 'ATTACHMENT', 'REFERRAL', 'POSTBACK']
    __metaclass__ = ABCMeta

    @safe_parse
    def __init__(self, entry: dict, mNum: int, messageType: str):
        messaging: dict = entry['messaging'][mNum]

        if messageType in self.SUPPORTED_MESSAGE_TYPES:
            self.messageType: str = messageType
        else:
            raise MessageParsingError("Unsupported message type")

        self.messageNum = mNum  # NOTE: This is deprecated
        self.pageId: str = entry['id']
        self.time: int = entry['time']
        self.senderId: str = messaging['sender']['id']
        self.recipientId: str = messaging['recipient']['id']
