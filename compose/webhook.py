# TODO: File-level docstrings

import flask
import json  # noqa
import logging  # TODO: Look into logging that filters sensitive info  # noqa
import os  # noqa
import sys
import traceback  # noqa

from typing import (List, Tuple)

from compose.recv.event import (process_event_messenger)
from compose.utils.errors import (gen_err_msg)
from compose.utils.keys import (verify_challenge, verify_signature)


compose_app = flask.Flask(__name__)
PROPAGATE_ERRORS = True


@compose_app.route("/", methods=['GET'])
def main_handle() -> str:
    """Return description of chatbot."""
    # TODO turn this into staticly delivered website
    print('Main handle accessed.')
    return ("", 200)


@compose_app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook() -> str:
    """
    Process POST and GET requests from the Messenger API.
    """

    request: flask.Request = flask.request
    response: Tuple[str, int] = ("", -1)

    try:
        if not verify_signature(request):
            response = ("Invalid request. Failed SHA-1 verification.", 403)

        elif request.method == 'GET':
            isVerified, respMsg = verify_challenge(request.args)
            response = (respMsg, 200 if isVerified else 403)

        elif request.method == 'POST':
            response = (process_post(request), 200)

        else:
            response = ("Unsupported HTTPS Verb.", 405)

    except Exception as e:
        # if PROPAGATE_ERRORS:
        #     raise
        print("\nReceived error\n")
        response = (f"{gen_err_msg(sys.exc_info(), e)}\nERROR: Not OK, but surviving. Check logs\n", 200)  # noqa: E501

    finally:
        return response


def process_post(request: flask.Request):
    """
    Process POST request and return
    """
    respMsg: str = ""
    results: List[Tuple[bool, dict]] = process_event_messenger(request)
    sentAll: bool = True

    for eNum, event in enumerate(results, start=1):
        for mNum, messageResult in enumerate(event, start=1):
            wasSent, response = messageResult
            if wasSent:
                respMsg += f"Sent msg {mNum} of {len(event)} in event {eNum}.\n"   # noqa
            else:
                sentAll = False
                respMsg += f'FAILED to send msg {mNum} of {len(event)} in event {eNum} with error: {response.get("error", "Could not get error.")}\n'  # noqa: E501
    return f"{{'success': '{respMsg}'}}" if sentAll else f"{{'error': '{respMsg}'}}"  # noqa: E501


if __name__ == '__main__':
    from .utils.keys import FLASK_ENV
    compose_app.run(debug=(FLASK_ENV == 'development'))


# TODO: Check out how pywit handles logging in __init__.py

    # # TODO: This should be in a unittest module
    # try:
    #     # Set up logging configuration
    #     logFile = os.path.join( '.',
    #         'compose',
    #         '.logs',
    #         '.bartbot-{}.log'.format('debug' if DEBUG else 'info'))
    #     os.makedirs(os.path.dirname(logFile), exist_ok=True)
    # except Exception as e:
    #     logging.error(f"Couldn't make log file {logFile}. Error: {e}")

    # logFormat = \
    #     "%(levelname)s:%(module)s:%(lineno)d %(message)s:%(asctime)s"

    # try:
    #     # # TODO: Check if uncommenting this breaks AWS Lambda
    #     # for handler in logging.root.handlers[:]:
    #     #     print(handler)

    #     logging.basicConfig(
    #         filename=logFile,
    #         format=logFormat,
    #         level=logging.DEBUG if DEBUG else logging.INFO)
    # except Exception as e:
    #     logging.error(f"Couldn't configure logfile. Error: {e}")

    # logging.info("\n\nS T A R T I N G   N E W   L O G\n\n")

    # # The above is a mess of logging.

    #     logging.info("E N D I N G   L O G")
    # logging.shutdown()
    # DEBUG = True
