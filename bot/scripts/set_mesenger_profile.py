import logging
import sys

from typing import (List, Tuple)

from compose.utils.requests import post
from compose.utils.urls import MESSENGER_PROFILE_API


get_started_data = {
    "get_started": {
        "payload": "Hello hello! Bartbot here. You can ask me about live schedules and weather [beta], or request a map. I'm constantly improving, so check back every now and then!"}}  # noqa: E501
greeting_data = {
    "greeting": [{
        "locale": "default",
        "text": "Hey {{user_first_name}}! Bartbot is here to " +
        "help you with your BART needs. What is BART? " +
        "Check out https://bart.gov/! "
    }, {
        "locale": "en_US",
        "text": "A one-stop shop for all your BART needs, " +
        "all on Messenger!"
    }]}
# TODO: Support multiple locales
home_url_data = {
    "home_url": {
        "url": "<URL_FOR_CHAT_EXTENSION>",
        "webview_height_ratio": "tall",
        "webview_share_button": "show",
        "in_test": False}}  # TODO: Set this to true in deployment

persistent_menu_data = {
    "persistent_menu": [{
        "locale": "default",
        "composer_input_disabled": False,
        "call_to_actions": [{
            "title": "Map",
            "type": "postback",
            "payload": "{'source': 'persistent_menu', 'request': 'map'}",
        }, {
            "title": "Travel",
            "type": "nested",
            "call_to_actions": [{
                "title": "Stations",
                "type": "nested",
                "call_to_actions": [{
                    "title": "Live Departures",
                    "type": "postback",
                    "payload": "{'source': 'persistent_menu', 'request': 'liveDepartures'}",  # noqa: E501
                }, {
                    "title": "Nearest Station [beta]",
                    "type": "postback",
                    "payload": "{'source': 'persistent_menu', 'request': 'nearestStation'}",  # noqa: E501
                }, {
                    "title": "Weather",
                    "type": "postback",
                    "payload": "{'source': 'persistent_menu', 'request': 'weather'}",  # noqa: E501
                }, {
                    "title": "Parking",
                    "type": "postback",
                    "payload": "{'source': 'persistent_menu', 'request': 'parking'}",  # noqa: E501
                }]
            }, {
                "title": "Cost",
                "type": "postback",
                "payload": "{'source': 'persistent_menu', 'request': 'cost'}",
            }, {
                "title": "Travel Time",
                "type": "postback",
                "payload": "{'source': 'persistent_menu', 'request': 'travel_time'}",  # noqa: E501
            }, {
                "title": "Delays & Accessibility",
                "type": "postback",
                "payload": "{'source': 'persistent_menu', 'request': 'delays_accessibility'}",  # noqa: E501
            }, {
                "title": "BART QuickPlanner",
                "type": "web_url",
                "url": "https://m.bart.gov/schedules/quickplanner",
            }]
        }, {
            "title": "Commutes",
            "type": "nested",
            "call_to_actions": [{
                "title": "My Commutes",
                "type": "postback",
                "payload": "{'source': 'persistent_menu', 'request': 'my_commutes'}",  # noqa: E501
            }, {
                "title": "Add Commute",
                "type": "postback",
                "payload": "{'source': 'persistent_menu', 'request': 'add_commute'}",  # noqa: E501
            }, {
                "title": "Settings",
                "type": "postback",
                "payload": "{'source': 'persistent_menu', 'request': 'settings'}",  # noqa: E501
            }]
        }],
    }],
}

# # 1 Map
# # 2 Travel
# #  2.1 Stations
# ## 2.1.1 Live Departures
# ## 2.1.2 Nearest Station [beta]
# ## 2.1.3 Weather
# ## 2.1.4 Parking
# #  2.2 Cost
# #  2.3 Travel Time
# #  2.4 Delays & Accessibility
# #  2.5 BART QuickPlanner
#   3 Commutes
# #  3.1 My Commutes
# #  3.2 Add Commute
# #  3.3 Settings
# #  3.3.1 Notification Style


persistent_menu_data_test = {
    "persistent_menu": [{
        "locale": "default",
        "composer_input_disabled": False,
        "call_to_actions": [{
            "title": "parent1",
            "type": "nested",
            "call_to_actions": [{
                "title": "nested11",
                "type": "nested",
                "call_to_actions": [{
                    "title": "nested111",
                    "type": "postback",
                    "payload": "nested111"
                }, {
                    "title": "nested112",
                    "type": "postback",
                    "payload": "nested112"
                }, {
                    "title": "nested113",
                    "type": "postback",
                    "payload": "nested113"
                }, {
                    "title": "nested114",
                    "type": "postback",
                    "payload": "nested114"
                }, {
                    "title": "nested115",
                    "type": "postback",
                    "payload": "nested115"
                }]
            }, {
                "title": "nested12",
                "type": "nested",
                "call_to_actions": [{
                    "title": "nested121",
                    "type": "postback",
                    "payload": "nested122"
                }, {
                    "title": "nested122",
                    "type": "postback",
                    "payload": "nested122"
                }, {
                    "title": "nested123",
                    "type": "postback",
                    "payload": "nested123"
                }, {
                    "title": "nested124",
                    "type": "postback",
                    "payload": "nested124"
                }, {
                    "title": "nested125",
                    "type": "postback",
                    "payload": "nested125"
                }]
            }, {
                "title": "nested13",
                "type": "nested",
                "call_to_actions": [{
                    "title": "nested131",
                    "type": "postback",
                    "payload": "nested131"
                }, {
                    "title": "nested132",
                    "type": "postback",
                    "payload": "nested132"
                }, {
                    "title": "nested133",
                    "type": "postback",
                    "payload": "nested133"
                }, {
                    "title": "nested134",
                    "type": "postback",
                    "payload": "nested134"
                }, {
                    "title": "nested135",
                    "type": "postback",
                    "payload": "nested135"
                }]
            }, {
                "title": "nested14",
                "type": "nested",
                "call_to_actions": [{
                    "title": "nested141",
                    "type": "postback",
                    "payload": "nested141"
                }, {
                    "title": "nested142",
                    "type": "postback",
                    "payload": "nested142"
                }, {
                    "title": "nested143",
                    "type": "postback",
                    "payload": "nested143"
                }, {
                    "title": "nested144",
                    "type": "postback",
                    "payload": "nested144"
                }, {
                    "title": "nested145",
                    "type": "postback",
                    "payload": "nested145"
                }]
            }, {
                "title": "nested15",
                "type": "postback",
                "payload": "cost"
            }]
        }, {
            "title": "parent2",
            "type": "nested",
            "call_to_actions": [{
                "title": "nested21",
                "type": "postback",
                "payload": "travel"
            }, {
                "title": "nested22",
                "type": "postback",
                "payload": "cost"
            }, {
                "title": "nested23",
                "type": "postback",
                "payload": "cost"
            }]
        }, {
            "title": "parent3",
            "type": "nested",
            "call_to_actions": [{
                "title": "nested34",
                "type": "nested",
                "call_to_actions": [{
                    "title": "nested341",
                    "type": "postback",
                    "payload": "nested341"
                }, {
                    "title": "nested342",
                    "type": "postback",
                    "payload": "nested342"
                }, {
                    "title": "nested343",
                    "type": "postback",
                    "payload": "nested343"
                }, {
                    "title": "nested344",
                    "type": "postback",
                    "payload": "nested344"
                }, {
                    "title": "nested345",
                    "type": "postback",
                    "payload": "nested345"
                }]
            }, {
                "title": "nested32",
                "type": "postback",
                "payload": "cost"
            }, {
                "title": "nested33",
                "type": "postback",
                "payload": "cost"
            }]
        }]
    }]
}
target_audience_data = {
    "target_audience": {
        "audience_type": "all"}}
# # NOTE: Comment above and uncomment below to whitelist
# "target_audience": {
#     "audience_type":"whitelist"
#     "countries": {
#     "whitelist": ["US", "CA"]}}}


def run_scripts(*scripts) -> List[bool]:
    """Runs all scripts provided in argument"""
    results = {}
    print(f"Running scripts: '{scripts}'")
    for script in scripts:
        print(f"Script: {script}")

        if script in 'get_started':
            results[script] = get_started()
        if script in 'greeting':
            results[script] = greeting()
        if script in 'home_url':
            results[script] = home_url()
        if script in 'persistent_menu':
            results[script] = persistent_menu()
        if script in 'target_audience':
            results[script] = target_audience()
    return results


def get_started() -> Tuple[bool, dict]:
    """Sets postback for Get Started"""
    logging.info("Setting Get Started")
    return post(MESSENGER_PROFILE_API, json=get_started_data)


def greeting() -> Tuple[bool, dict]:
    """Sets the greeting for the Get Started page"""
    logging.info("Setting greeting")
    return post(MESSENGER_PROFILE_API, json=greeting_data)


def home_url() -> Tuple[bool, dict]:
    """Sets the home URL of the bot"""
    logging.info("Setting home URL")
    return post(MESSENGER_PROFILE_API, json=home_url_data)


def persistent_menu() -> Tuple[bool, dict]:
    """Sets the style and elements of the persistent menu"""
    logging.info("Setting persistent menu")
    return post(MESSENGER_PROFILE_API, json=persistent_menu_data)


def target_audience() -> Tuple[bool, dict]:
    """Sets the audience that this bot is accessible to"""
    logging.info("Setting target audience")
    return post(MESSENGER_PROFILE_API, json=target_audience_data)


if __name__ == '__main__':
    scripts = list(sys.argv)
    print(run_scripts(scripts))
