import logging

from typing import (List, Optional)

from .message import (Coordinate, Message, safe_parse)


class Payload():

    @safe_parse
    def __init__(self, attachment: dict, text: str):
        self.attmType: str = attachment['type'].upper()
        self.text: Optional[str] = text \
            if self.attmType == 'FALLBACK' else None
        self.title: Optional[str] = attachment['title'] \
            if self.attmType == 'FALLBACK' else None
        if self.attmType == 'LOCATION':
            coordinates: Optional[dict] = attachment['payload'].get(
                'coordinates')
            self.coordinates: Coordinate = (coordinates['long'],
                                            coordinates['lat']) \
                if coordinates else None
        else:
            self.url = attachment['url'] if self.attmType == 'FALLBACK' \
                else attachment['payload'].get('url')


class Attachment(Message):
    SUPPORTED_ATTACHMENT_TYPES = ['IMAGE', 'VIDEO', 'AUDIO', 'FILE',
                                  'LOCATION', 'FALLBACK']

    @safe_parse
    def __init__(self, entry: dict, mNum: int):
        super().__init__(entry=entry, mNum=mNum, messageType='ATTACHMENT')

        message = entry['messaging'][mNum]['message']

        self.messageId: str = message['mid']
        self.attachments: List[Payload] = []

        # Parse each attachment and append to self.attachments
        for attachment in message['attachments']:
            attmType = attachment['type']
            if not isinstance(attmType, str) or attmType.upper() not in \
                    self.SUPPORTED_ATTACHMENT_TYPES:
                logging.warning(
                    'Received unsupported attachment type. Skipping.')
            self.attachments.append(Payload(attachment, message.get('text')))
