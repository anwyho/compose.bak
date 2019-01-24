import json  # noqa
import logging

from time import (sleep)
from typing import (List, Optional, Tuple)

from compose.utils.requests import (post)
from compose.utils.urls import (MESSAGES_API)


class InvalidResponseStructureError(Exception):
    """
    Raised when Response has incorrect structure or is not ready to be sent.
    """
    pass


class Response:

    ATTACHMENT_TYPES: List[str] = [
        'image', 'audio', 'video', 'file', 'template']
    MAX_QUICK_REPLIES: int = 11
    MAX_TIMEOUT: float = 10.0
    MESSAGING_TYPES: List[str] = ['RESPONSE', 'UPDATE', 'MESSAGE_TAG']
    NOTIFICATION_TYPES: List[str] = [
        'regular', 'silent_push', 'no_push', '']
    QUICK_REPLY_PAYLOAD_CHAR_lIMIT = 1000
    QUICK_REPLY_TYPES: List[str] = [
        'text', 'location', 'user_phone_number', 'user_email']
    TAGS: List[str] = [
        'community_alert',
        'confirmed_event_reminder',
        'non_promotional_subscription',
        'transportation_update',
        'feature_functionality_update',
        '']
    SENDER_ACTIONS: List[str] = ['mark_seen', 'typing_on', 'typing_off', '']

    def __init__(self,
                 apiUrl: Optional[str] = MESSAGES_API,
                 description: str = "default",
                 data: Optional[dict] = {},
                 dryRun: bool = False,
                 timeout: float = 0):
        self.apiUrl: Optional[str] = apiUrl
        self.description: str = description
        self.timeout: float = timeout
        self._data: dict = data
        self._dryRun: bool = dryRun
        self._chainedResponse = None
        self._passingChecks: bool = False

    @classmethod
    def from_message(cls, message, withController):
        return withController(message=message).produce_responses()

    def _pre_send_check(self):
        """
        Check readiness of data before sending. Raise exceptions when
            something is wrong. Always returns True otherwise.
        """

        # TODO: Add a pre_send_check to ResponseBuilder that checks
        #   for quick_replies on the not-last-response
        # if self._chainedResponse and self.quick_replies

        # TODO: Check if everything is ready
        # NOTE: This needs to apply to both Send API objects and other objects
        if False:
            raise InvalidResponseStructureError("Response has incorrect structure and is not ready to be sent.")  # noqa: E501

        self._passingChecks = True
        return True

    @property
    def passedChecks(self):
        self._pre_send_check()
        return self._passingChecks

    def send(self, inChain: bool = False) -> List[Tuple[bool, dict]]:
        """
        Check if response passes checks and then send current
            response and any chained responses. Return a list of
            bools depicting the success or failure of each successive
            send.
        """
        if self._timeout > 0:
            sleep(self._timeout)

        results: List[Tuple[bool, Optional[dict]]] = []

        if self._dryRun:
            res = f"DRY-RUN - {self.description}"
            print(res)
            results.append((True, res))
            results.extend(self.send_chained_response())

        elif self.passedChecks:
            results.append(post(self.apiUrl, json=self._data))
            if results[0][0]:  # Successfully sent
                print(f"sent - {self.description}")
            else:  # Failed to send
                print(f"FAILED - {self.description}\n\t{results[0][1]}")
            results.extend(self.send_chained_response())

        else:
            logging.warning("Attempted to send, unsuccessfully.")

        return results

    @property
    def timeout(self) -> float:
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: float) -> None:
        self._timeout = timeout if timeout < self.MAX_TIMEOUT else 0

    def send_chained_response(self) -> List[Tuple[bool, dict]]:
        return self._chainedResponse.send(inChain=True) \
            if isinstance(self._chainedResponse, Response) else []
