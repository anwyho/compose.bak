import unittest

from requests import (Response)  # noqa

from compose.test import (app_endpoint, EntityBuilder, RequestBuilder)  # noqa

from .parser import (BartbotEntityParser, get_datetime)  # noqa


class TestWit(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_datetime_conversion(self) -> None:
        pass

    # def test_greeting(self) -> None:
    #     """
    #     Simple greeting test that expects a 200 OK response.
    #     """

    #     data: dict = RequestBuilder().add_text("Hello there.").build()
    #     response: Response = app_endpoint('POST', json=data)
    #     # print(response.content)
    #     # self.assertTrue(ok, 'Must receive OK from response.')
    #     self.assertEqual(response.status_code, 200,
    #                      'POST should go through successfully.')
    #     self.assertNotIn('error', response,
    #                      'Error should not be in response.')


travel_morning = {
    "_text": "When's the next train from warm springs to union city tomorrow morning?",  # noqa
    "entities": {
        "orig": [
            {
                "confidence": 0.99944644516303,
                "value": "WARM",
                "type": "value"
            }
        ],
        "dest": [
            {
                "confidence": 0.99151438846078,
                "value": "UCTY",
                "type": "value"
            }
        ],
        "dep": [
            {
                "confidence": 0.91889398788601,
                "values": [
                    {
                        "to": {
                            "value": "2019-01-27T12:00:00.000-08:00",
                            "grain": "hour"
                        },
                        "from": {
                            "value": "2019-01-27T04:00:00.000-08:00",
                            "grain": "hour"
                        },
                        "type": "interval"
                    }
                ],
                "to": {
                    "value": "2019-01-27T12:00:00.000-08:00",
                    "grain": "hour"
                },
                "from": {
                    "value": "2019-01-27T04:00:00.000-08:00",
                    "grain": "hour"
                },
                "type": "interval"
            }
        ],
        "intent": [
            {
                "confidence": 0.99999998373383,
                "value": "travel"
            }
        ]
    },
    "msg_id": "1nVrB9egw7r3Vtnlc"
}


if __name__ == "__main__":
    unittest.main()
