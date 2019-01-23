import json  # noqa
import logging  # noqa

from typing import (Optional)

from .message import (Message, MessageParsingError, ParamType, safe_parse)  # noqa


class Referral(Message):
    REF_SOURCES = ['MESSENGER_CODE', 'DISCOVER_TAB', 'ADS',
                   'SHORTLINK', 'CUSTOMER_CHAT_PLUGIN']
    REF_TYPES = ['OPEN_THREAD']

    @safe_parse
    def __init__(self, entry: dict, mNum: int, inPostback: bool = False):
        referral = entry['messaging'][mNum]['referral']

        if not isinstance(referral.get('source'), str) or \
                not isinstance(referral.get('type'), str) or \
                referral.get('source').upper() not in self.REF_SOURCES or \
                referral.get('type').upper() not in self.REF_TYPES:
            raise MessageParsingError(
                "Referrals must contain a valid source and type")

        if not inPostback:
            super().__init__(entry=entry, mNum=mNum, messageType='REFERRAL')

        self.refSource: str = referral['source'].upper()
        self.refType: str = referral['type'].upper()
        self.ref: Optional[str] = referral.get('ref')
        if self.ref:
            if self.refSource == 'CUSTOMER_CHAT_PLUGIN':
                self.refererUri: str = referral.get('referer_uri')
            elif self.refSource == 'ADS':
                self.adId: str = referral.get('ad_id')
