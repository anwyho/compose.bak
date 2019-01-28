import unittest

from requests import (Response)  # noqa

from bot.utils.keys import (FB_PID)

from compose.test import (app_endpoint, RequestBuilder)  # noqa


class TestIntegration(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    # def test_empty_post(self) -> None:
    #     """
    #     Sends empty and erroneous POST requests expecting 200 status.
    #     """

    #     response: Response = app_endpoint('POST', json={})
    #     self.assertEqual(response.status_code, 200,
    #                      'Empty post should still return 200 OK status.')

    def test_greeting(self) -> None:
        """
        Simple greeting test that expects a 200 OK response.
        """
        data: dict = RequestBuilder(
            pageId=FB_PID, senderId="2153980617965043"
        ).add_text("Hello there.").build()
        response: Response = app_endpoint('POST', json=data)

        self.assertEqual(response.status_code, 200,
                         'POST should go through successfully.')

    def test_batch(self) -> None:
        """
        Integration test that sends 8 batched messages expected a
            200 OK response.
        """
        data: dict = RequestBuilder(
            pageId=FB_PID, senderId="2153980617965043") \
            .add_text("Batch integration test 1") \
            .add_text("Batch integration test 2") \
            .add_text("Batch integration test 3") \
            .add_text("Batch integration test 4") \
            .add_text("Batch integration test 5") \
            .add_text("Batch integration test 6") \
            .add_attachment() \
            .add_text("Batch integration test 8") \
            .build()
        response: Response = app_endpoint('POST', json=data)

        self.assertEqual(response.status_code, 200,
                         'Batched POSTs should go through successfully.')


if __name__ == "__main__":
    unittest.main()
