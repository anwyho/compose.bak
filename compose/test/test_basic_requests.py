import os
import unittest

from requests import (Response)
from typing import (Dict)

from .test_utils import app_endpoint
# from compose.test.configs import (TEST_URL)


class TestBasicRequests(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_valid_challenge(self) -> None:
        """
        Sends a challenge to webhook with a valid token expecting a
            200 status and an echo of the challenge.
        """

        CHALLENGE = 'challenge_should_be_accepted'

        validParams: Dict[str] = {
            'hub.mode': 'subscribe',
            'hub.challenge': CHALLENGE,
            'hub.verify_token': os.environ.get('FB_VERIFY_TOK')
        }
        response: Response = app_endpoint('GET', params=validParams)
        self.assertEqual(response.status_code, 200,
                         'GET endpoint should always return 200 OK on successful verification.')  # noqa: E501
        self.assertEqual(response.content.decode('utf-8'),
                         CHALLENGE,
                         'Response should return challenge sent')

    def test_invalid_challenge(self) -> None:
        """
        Sends a challenge to webhook with an in valid token expecting
            a 403 status and an error message.
        """

        CHALLENGE = 'challenge_should_be_rejected'

        invalidToken: str = 'INVALID_TOKEN'
        self.assertNotEqual(invalidToken, os.environ.get('FB_VERIFY_TOK'))
        invalidParams: Dict[str] = {
            'hub.mode': 'subscribe',
            'hub.challenge': CHALLENGE,
            'hub.verify_token': invalidToken
        }
        response: Response = app_endpoint('GET', params=invalidParams)
        self.assertEqual(response.status_code, 403,
                         'GET endpoint should not return 200 OK on unsuccessful verification.')  # noqa: E501
        self.assertNotEqual(response.content.decode('utf-8'),
                            CHALLENGE,
                            'Response should not return challenge sent.')

    def test_non_get_post(self) -> None:
        """
        Sends a request that is neither GET nor POST expecting a 204 status.
        """
        pass
        response: Response = app_endpoint('PUT')
        self.assertEqual(response.status_code, 405)
        response: Response = app_endpoint('DELETE')
        self.assertEqual(response.status_code, 405)
        response: Response = app_endpoint('HEAD')
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
