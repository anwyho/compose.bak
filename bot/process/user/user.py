import json  # noqa
import logging  # noqa

from typing import (List, Optional)  # noqa

from .abstract_user import (AbstractUser)
from compose.utils.requests import (get)  # noqa
from compose.utils.urls import (MESSENGER_USER_API)  # noqa


class BartbotUser(AbstractUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def retrieve_session_data(self):
        pass


# TODO: Cache BART cost/other stuff in DynamoDB
bartCache = {}

# TODO: Throw this into DynamoDB?
userSessionData = {
    '{userId}': {
        'user': {
            'fbId': '{fbId}',
            'first_name': '{firstName}',
            'preferred_name': '',
            'last_name': '{lastName}',
            'initial_locale': 'en_US',
            'current_locale': '',
            'join_date': '{joinDate}',
        },
        'last_session_time': '{lastSessionTime}',
        'last_request_time': '{lastRequestTime}',
        'in_session': False,
        'session_data': [{
            'session_init_time': '{sessionInitTime}',
            'intent': '{intent}',
            'sta_orig': '{staOrig}',
            'sta_dest': '{staDest}',
            'time_dep': '{timeDep}',
            'time_arr': '{timeArr}',
            'decision': '{decision}',
            'greetings': False,
            'thanks': False,
            'bye': False,
            'visible_quick_replies': {
                # 'cost': '{}'  # Info on state
            },
            'session_payload': '',
        }, {
            'session_init_time': '{sessionInitTime}',
            'intent': '{intent}',
            'sta_orig': '{staOrig}',
            'sta_dest': '{staDest}',
            'time_dep': '{timeDep}',
            'time_arr': '{timeArr}',
            'decision': '{decision}',
            'greetings': False,
            'thanks': False,
            'bye': False,
            'session_payload': '',
        }],
        'station_aliases': {
            '{alias}': '{station}',
        },
        'metadata': {
            'achievements': {
                'TODO': 'change behavior on metadata achievements.'
            },
        }
    }
}

# TODO: Throw this into S3?
userMetadata = {
    '{userId}': {
        'messages': {
            'sent': 0,
            'received': 0,
            'completed_session': 0,
            'left_before_session_end': 0,
        },
        'trips': {
            '12TH': {
                'station_intents': {
                    'travel': 0,
                },
                '16TH': {
                    'last_date_queried': '{lastDateQueried}',
                    'unique_days_queried_within_interval': 0,
                    'total_orig_to_dest': 0,
                    'hour_departing': {
                        0: 0,
                    },
                },
            },
        },
        'total_intents': {
            'travel': 0,
        },
        'stations': {
            'orig': {'12TH': 0},
            'dest': {'12TH': 0},
            'none': {'12TH': 0},
        },
    }
}
