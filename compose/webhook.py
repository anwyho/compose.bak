# TODO: File-level docstrings

import flask
import json  # noqa
import logging  # TODO: Look into logging that filters sensitive info
import os
import sys
import traceback

from typing import (List)

from compose.recv.event import (process_event_messenger)
from compose.utils.keys import (verify_challenge, verify_signature)


compose_app = flask.Flask(__name__)

# bartbotGithubHtml: str = '<a href="http://github.com/anwyho/bartbot">github.com/anwyho/bartbot</a>'  # noqa: E501
# APP_HANDLE_TEXT: str = f'Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out {bartbotGithubHtml} for more details.'  # noqa: E501


@compose_app.route("/", methods=['GET'])
def main_handle() -> str:
    """Return description of chatbot."""
    # TODO turn this into staticly delivered website
    print('Main handle accessed.')
    return ("", 200)
    # global APP_HANDLE_TEXT
    # return APP_HANDLE_TEXT


@compose_app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook() -> str:
    """
    Process POST and GET requests from the Messenger API.
    """

    try:
        request: flask.Request = flask.request

        if not verify_signature(request):
            return ("Invalid request. Failed SHA-1 verification.", 403)

        if request.method == 'GET':
            isVerified, respMsg = verify_challenge(request.args)
            return (respMsg, 200 if isVerified else 403)
        elif request.method == 'POST':
            return (process_post(request), 200)
        else:
            return ("Unsupported HTTPS Verb.", 405)

    except Exception as e:
        print("Received error")
        return (f"{generate_error_message(sys.exc_info(), e)}\nERROR: Not OK, but surviving. Check logs\n", 200)  # noqa: E501


def process_post(request: flask.Request):
    """
    Process POST request and return
    """
    respMsg: str = ""
    results: List[dict] = process_event_messenger(request)
    sentAll: bool = True
    for event in results:
        for mNum, messageResult in enumerate(event, start=1):
            wasSent, response = messageResult
            if wasSent:
                respMsg += f"Sent msg {mNum} of {len(event)}.\n"
            else:
                sentAll = False
                respMsg += f'FAILED to send msg {mNum} with error: {response.get("error", "Could not get error.")}\n'  # noqa: E501
    print(respMsg)
    return "{{'success': 'All clear.'}}" if sentAll else f"{{'error': 'Failed to send all messages.\n{respMsg}'}}"  # noqa: E501


def generate_error_message(execInfo, err: Exception) -> str:
    # TODO: typing for execInfo ^
    """
    Accepts sys.exec_info and error e and converts to a readable string.
    """

    exc_type, _, exc_tb = execInfo
    traceback.print_tb(exc_tb)
    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    errorMsg: str = f"An unexpected error occurred. Error: {err}. Error info: {exc_type}, {filename}, {exc_tb.tb_lineno}"  # noqa: E501
    logging.debug(errorMsg)
    return errorMsg


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
