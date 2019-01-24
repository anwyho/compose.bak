import hashlib
import hmac
import flask
import os

from typing import (Tuple)

# TODO: Refresh all keys

MISSING_KEY_MSG = "Key not found."

# Facebook
FB_PAGE_ACCESS: str = os.environ.get(
    'FB_PAGE_ACCESS', MISSING_KEY_MSG)
FB_PAGE_ACCESS_2: str = os.environ.get(
    'FB_PAGE_ACCESS_2', None)
FB_VERIFY_TOK: str = os.environ.get(
    'FB_VERIFY_TOK', MISSING_KEY_MSG)

# Debug
FLASK_ENV: str = os.environ.get('FLASK_ENV', "production")


def gen_app_secret_proof():
    """Calculate FB app secret proof from SHA256."""
    print(f"Generating app secret proof...")
    _pudding = hmac.new(FB_PAGE_ACCESS_2.encode('utf-8'),
                        msg=FB_PAGE_ACCESS.encode('utf-8'),
                        digestmod=hashlib.sha256).hexdigest()
    return _pudding


def verify_signature(request: flask.Request) -> bool:
    """Verify SHA-1 of message"""
    # TODO: Potential bug in the future
    if FLASK_ENV is not 'development' and FB_PAGE_ACCESS_2 is not '':
        print('Verifying signature...')
        # TODO: Verify SHA-1
        return True
    else:
        print(f'No signature to compare to.')
        return True


def verify_challenge(queryParams: dict) -> Tuple[bool, str]:
    """
    Verify and fulfill Messenger Platform GET challenge.
    """

    print(f'Verifying challenge...')
    # True if request contains valid request mode, valid verify token,
    #   and challenge string.
    if queryParams.get('hub.verify_token') == FB_VERIFY_TOK and \
            queryParams.get('hub.mode') == 'subscribe' and \
            isinstance(queryParams.get('hub.challenge'), str):
        print(f'Challenge verified.')
        return (True, queryParams['hub.challenge'])
    else:
        print(f'Challenge rejected.')
        return (False, 'Invalid request or verification token.\n')
