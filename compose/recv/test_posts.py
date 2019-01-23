
import unittest
from requests import (Response)
from compose.test.test_utils import (app_endpoint, RequestBuilder)


class TestPosts(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_empty_post(self) -> None:
        """
        Sends empty and erroneous POST requests expecting 200 status.
        """

        response: Response = app_endpoint('POST', json={})
        self.assertEqual(response.status_code, 200,
                         'Empty post should still return 200 OK status.')

    def test_greeting(self) -> None:
        """
        Simple greeting test that expects a 200 OK response.
        """

        data: dict = RequestBuilder().add_text("Hello there.").build()
        response: Response = app_endpoint('POST', json=data)
        # print(response.content)
        # self.assertTrue(ok, 'Must receive OK from response.')
        self.assertEqual(response.status_code, 200,
                         'POST should go through successfully.')
        self.assertNotIn('error', response,
                         'Error should not be in response.')


if __name__ == "__main__":
    unittest.main()
