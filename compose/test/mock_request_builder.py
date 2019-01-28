
from typing import (List)


class RequestBuilder:
    def __init__(self,
                 pageId: str = '<PAGE_ID>',
                 senderId: str = '<SENDER_ID>'):
        self.pageId: str = pageId
        self.senderId: str = senderId
        self.messages: List[dict] = []

    def build(self) -> dict:
        self.request = {
            "object": "page",
            "entry": [{
                "id": self.pageId,
                "time": 1,
                "messaging": self.messages
            }]
        }
        self.messages = []
        return self.request

    def add_text(self, text: str) -> dict:
        textMessage: dict = {
            "sender": {"id": self.senderId},
            "recipient": {"id": self.pageId},
            "timestamp": 1,
            "message": {
                "mid": "<MSG_ID>",
                "seq": 1,
                "text": text,
            }
        }
        self.messages.append(textMessage)
        return self

    def add_attachment(self) -> dict:
        attachmentMessage: dict = {
            "sender": {"id": self.senderId},
            "recipient": {"id": self.pageId},
            "timestamp": 1,
            "message": {
                "mid": "<MSG_ID>",
                "seq": 1,
                "sticker_id": 1,
                "attachments": [{
                    "type": "image",
                    "payload": {
                        "url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/39178562_1505197616293642_5411344281094848512_n.png?_nc_cat=1&_nc_ad=z-m&_nc_cid=0&oh=dd1b37bf025c96a8f7144fa6a30c4f62&oe=5BF19F75",  # noqa: E501
                        "sticker_id": 1
                    }
                }]
            }
        }
        self.messages.append(attachmentMessage)
        return self

    def add_postback(self):
        pass
