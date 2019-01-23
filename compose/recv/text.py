from typing import (Optional)

from .message import (Message, safe_parse)


class Text(Message):

    @safe_parse
    def __init__(self, entry: dict, mNum: int):
        super().__init__(entry=entry, mNum=mNum, messageType='TEXT')
        message = entry['messaging'][mNum]['message']
        self.messageId: str = message['mid']
        self.text: str = message['text']
        self.quickReply: Optional[str] = message.get(
            'quick_reply', {}).get('payload')
