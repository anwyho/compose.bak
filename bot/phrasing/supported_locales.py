"""This module contains bartbot-specific locale information."""

#  _                _   _           _
# | |__   __ _ _ __| |_| |__   ___ | |_
# | '_ \ / _` | '__| __| '_ \ / _ \| __|
# | |_) | (_| | |  | |_| |_) | (_) | |_
# |_.__/ \__,_|_|   \__|_.__/ \___/ \__|
# Get all your BART info from your Messenger app!

# TODO: Turn this file into a YAML and load it into locales with PyYAML?

DEFAULT_LOCALE = "en_us"

SUPPORTED_LOCALES: dict = {
    "en_us": "en_US",
    "en_gb": "en_US",
    "en_ud": "en_US",
}

FUTURE_SUPPORTED_LOCALES: dict = {
    "es_la": "es_LA",
    "ja_jp": "ja_JP",
    "ja_ks": "ja_JP",
    "zh_cn": "zh_CN",
    "zh_hk": "zh_HK_TW",
    "zh_tw": "zh_HK_TW",
}
