import flask
import json
import logging
import sys

from concurrent.futures import (Future, ThreadPoolExecutor)
from typing import (List, Optional, Tuple)

import compose.process as proc
import compose.recv as recv

from compose.send.response import (Response)
from compose.utils.errors import (gen_err_msg)

# Number of messages in batch before activating multithreading
SEQ_PROCESS_MSG_THRESH = 1


def process_event_messenger(request: flask.Request) -> List[dict]:
    """Collects and processes events. Returns a list of JSONs of responses"""

    data: Optional[dict] = request.get_json(silent=True)
    entryList: List[dict] = data.get('entry', []) if data else[]

    if len(entryList) == 0:
        raise KeyError("Empty request.")
    # Guaranteed, there will only be one entry. source: # TODO
    if not (len(entryList) == 1 and isinstance(entryList[0], dict)):
        raise KeyError("Received entry had an unexpected structure.")

    entry: dict = entryList[0]
    objType: str = data.get('object').lower()
    results: List[dict] = []

    if objType == 'page':
        results = page_event(entry)
    elif objType == 'user':
        results = user_event(entry)
    else:
        raise KeyError("Received entry had an unexpected object type.")

    return results


def user_event(entry: dict) -> List[Tuple[bool, dict]]:
    """Process an event from User Graph API."""
    # results = []  # collects results of events
    # events = find_user_events(entry)
    # results.extend(...)
    return []


def page_event(entry: dict) -> List[List[Tuple[bool, dict]]]:
    """For each message in an entry, create and send a response."""
    # Controller cannot be directly imported because of circular imports
    controller: proc.Controller = proc.import_controller()
    results: list = []

    # Handle message sequentially
    if len(entry.get('messaging', '')) <= SEQ_PROCESS_MSG_THRESH:
        results: List[dict] = []
        for message in get_messages(entry):
            results.append(handle_message(message, controller))

    # Handle message concurrently
    else:
        results: list = []
        with ThreadPoolExecutor(max_workers=8) as p:
            # NOTE to future self: Turning this into a generator
            #   kills the concurrency since the list comprehension
            #   evaluates the statements here.
            # TODO: Check if removing `*( )` breaks code
            futures: List[Future] = []
            for message in get_messages(entry):
                futures.append(
                    p.submit(handle_message, *(message, controller)))

        # Wait for all futures to finish
        for future in futures:
            while True:
                if future.done():
                    result = future.result()
                    if isinstance(result, Future):
                        future = result
                    else:
                        results.append(result)
                        break

    return list(results)


def handle_message(message: recv.Message,
                   controllerType: proc.AbstractController) \
        -> List[Tuple[bool, dict]]:
    """Create and send Responses and return the output."""

    try:
        response: Response = Response.from_message(
            message=message,
            withController=controllerType)
        result = response.send()
        return result
    except Exception as e:
        gen_err_msg(sys.exc_info(), e)


def get_messages(entry: dict) -> recv.Message:
    """
    Get specifically-typed instantiated messages from an entry
        depending on distinguishing factors in each message.
    """

    messaging = entry.get('messaging')
    if not (isinstance(messaging, list) and len(messaging)):
        logging.warning(f"Couldn't find any page events in entry.")
        logging.debug(f"{json.dumps(entry, indent=2)}")
        return

    for msgNum, message in enumerate(messaging):
        messageType, messageInstance = None, None

        # Attachments gets precedence because it can also have text
        if 'attachments' in message.get('message', {}):
            messageType = recv.Attachment
        # Echo gets precedence over Text for the same reason as Attachments
        elif message.get('message', {}).get('is_echo'):
            # TODO messageType = recv.Echo
            pass
        elif 'text' in message.get('message', {}):
            messageType = recv.Text
        elif 'postback' in message:
            messageType = recv.Postback
        elif 'referral' in message:
            messageType = recv.Referral
        else:
            logging.warning(f"Couldn't identify Message type. Skipping.")
            logging.debug(f"{json.dumps(entry, indent=2)}")

        # Convert message type into message instance
        if messageType is not None:
            try:
                messageInstance = messageType(entry=entry, mNum=msgNum)
            except recv.MessageParsingError as e:
                gen_err_msg(sys.exc_info(), e)
                logging.warning(f"Failed to parse message. Error: {e}")
                logging.debug(json.dumps(entry))
                messageInstance = None

        if messageInstance:
            yield messageInstance
