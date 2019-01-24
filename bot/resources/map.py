import json
import logging
import os

from typing import Optional

from compose.send.response import (Response)
from compose.utils.urls import MESSAGE_ATTACHMENTS_API


BART_MAP_URL = "https://github.com/anwyho/bart-map/blob/master/BART_cc_map.png?raw=true"  # noqa: E501
BART_MAP_FILE = os.path.join(
    'bot', 'resources', 'images', 'bart_map_id.txt')

# HACK: Very specific to bartbot map
# TODO: Improve this function to work for any given attachment


def yield_map_id(
        forceRefresh=False,
        writeCache: os.path = BART_MAP_FILE) -> Optional[str]:
    """
    Yield local copy of map ID and then a refreshed version.
    Saves attachment to FB for cached map.
    Places attachment ID into 'compose/resources/images/bart_map_id.txt'.
    """

    # Yields locally sourced map ID
    if forceRefresh:
        yield None
    else:
        mapId = read_local(writeCache)
        yield mapId

    # Upload attachment from GitHub URL
    mapId = post_from_url()
    if mapId is not None:
        write_local(mapId, writeCache)

    # TODO: Upload attachment from S3 Bucket
    if mapId is None:
        mapId = post_from_S3()

    yield mapId


def read_local(writeCache: os.path) -> Optional[str]:
    """Tries to read attachment ID from file"""
    try:
        with open(writeCache, 'r') as f:
            mapId = f.read()

    except IOError as e:
        logging.warning("Couldn't retreive attachment ID from file " +
                        f"{writeCache}. Error: {e}")
        mapId = None

    else:
        if mapId.isdigit():
            logging.info("Successfully read in attachment ID")
        else:
            logging.warning("Invalid attachment ID in file")
            logging.debug(f"mapId = {mapId}")
            mapId = None

    finally:
        return mapId


def post_from_url() -> Optional[str]:
    """Tries to POST url of original map to Messenger Attachments"""
    data = {
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "is_reusable": 'true',
                    "url": BART_MAP_URL}}}}
    isOk, resp = Response(apiUrl=MESSAGE_ATTACHMENTS_API, data=data).send()[0]
    if isOk and 'attachment_id' in resp:
        return resp['attachment_id']
    else:
        logging.warning("Couldn't retrieve attachment ID from Messenger")
        logging.debug(f"resp: {json.dumps(resp,indent=2)}")
        return None


def write_local(mapId: str, writeCache: os.path) -> bool:
    """Tries to cache attachment ID to a local file"""
    try:
        with open(writeCache, 'w') as f:
            f.write(mapId)
    except Exception as e:
        logging.warning("Couldn't write attachment ID to " +
                        f"file {writeCache}. Received error {e}.")
        return False
    else:
        logging.info(f"Wrote map attachment ID to file {writeCache}")
        return True


def post_from_S3() -> Optional[str]:
    # TODO: Not implemented
    raise NotImplementedError()


if __name__ == '__main__':
    print(yield_map_id(forceRefresh=True))
