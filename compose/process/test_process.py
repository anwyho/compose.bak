import unittest

import compose.process as proc

from compose.test.test_utils import (app_endpoint, RequestBuilder)  # noqa


class TestController(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_successful_controller_import(self) -> None:
        """
        Sends empty and erroneous POST requests expecting 200 status.
        """

        # BUG: Find out why this doesn't work. Bartbot Controller should inherit from Controller.  # noqa: E501
        self.assertTrue(issubclass(proc.import_controller(), proc.Controller),
                              "compose.process.import_controller should return a subclass of Controller.")  # noqa: E501


if __name__ == "__main__":
    unittest.main()
