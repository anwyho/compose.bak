import requests

from .test_configs import (TEST_URL)


def app_endpoint(*args, **kwargs):
    return requests.request(method=args[0] if args else kwargs['method'],
                            url=TEST_URL, **kwargs)
