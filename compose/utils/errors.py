
import logging
import json
import os
import sys
import traceback
import wrapt


def handle_request_error(response: dict) -> bool:
    """
    Returns True if no error and False if error.
    Handles error and outputs to logs.
    """

    logging.debug(f"Response: {json.dumps(response,indent=2)}")

    return 'error' not in response


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


@wrapt.decorator
def catch_here(wrapped, instance, args, kwargs):
    try:
        return wrapped(*args, **kwargs)
    except Exception as e:
        generate_error_message(sys.exec_info(), e)
