
import json  # noqa
import logging  # noqa

from typing import (Optional)

from .message import (Message, MessageParsingError, ParamType, safe_parse)  # noqa
from .referral import (Referral)


class Postback(Message):

    @safe_parse
    def __init__(self, entry: dict, mNum: int):
        super().__init__(entry=entry, mNum=mNum, messageType='POSTBACK')
        postback = entry['messaging'][mNum]['postback']
        self.title: str = postback['title']
        self.payload = postback['payload']
        try:
            self.referral: Optional[Referral] = Referral(
                entry=entry, mNum=mNum, inPostback=True)
        except MessageParsingError:
            self.referral: Optional[Referral] = None
