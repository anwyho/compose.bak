import pytest  # noqa

from requests import (Response)  # noqa

from bot.utils.keys import (FB_PID)

from compose.test.test_utils import (app_endpoint, RequestBuilder)  # noqa


def test_greeting():
    data: dict = RequestBuilder(
        pageId=FB_PID, senderId="2153980617965043"
    ).add_text("Hello there.").build()
    response: Response = app_endpoint('POST', json=data)
    assert response.status_code == 200
