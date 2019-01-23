
import json  # noqa
import logging  # noqa

from abc import (ABC, abstractmethod)
from typing import (List, Optional)

from .response_utils import (CondSetter as sets)
# from .response_attachment import (ShareTemplate)


class Button(ABC):
    """
    A button to be nested within a Messenger Template or Message.
    """

    BUTTON_TYPES: List[Optional[str]] = [
        'web_url',
        'postback',
        'element_share',
        'phone_number',
    ]

    BUTTON_TITLE_CHAR_LIMIT = 20

    @classmethod
    def make_button(cls, buttonType: str, **buttonInitArgs):
        """
        Create a button of buttonType with specific initialization
            args.
        """
        if not isinstance(buttonType, str) or \
                buttonType not in cls.BUTTON_TYPES:
            raise ValueError(
                f"Attempted to make unsupported button type {buttonType}.")

        buttonType: str = buttonType.lower()
        if buttonType == 'web_url':
            return UrlButton(**buttonInitArgs)
        elif buttonType == 'postback':
            return PostbackButton(**buttonInitArgs)
        elif buttonType == 'element_share':
            return ShareButton(**buttonInitArgs)
        elif buttonType == 'phone_number':
            return CallButton(**buttonInitArgs)
        else:
            raise ValueError(
                f"Attempted to make unsupported button type {buttonType}.")

    @abstractmethod
    def build(self) -> dict:
        """
        Build button as a dictionary to be nested within a message.
        """
        pass


# DONE
class UrlButton(Button):
    """Builds a URL button to be nested in a message."""

    TITLE_CHAR_LIMIT = 20
    WEB_VIEW_HEIGHT_RATIOS = ['compact', 'tall', 'full']

    def __init__(self,
                 text: str,
                 url: str,
                 messengerExtensions: bool = False,
                 fallbackUrl: Optional[str] = None,
                 webviewHeightRatio: Optional[str] = None,
                 webviewShareButton: bool = True) -> None:
        self._button: dict = {}

        self.buttonType: str = 'web_url'
        sets.with_max_string_len(self, '_title', text,
                                 maxLen=self.TITLE_CHAR_LIMIT)
        sets.if_exists(self, '_url', url)
        sets.if_in_list(self, '_webviewHeightRatio', webviewHeightRatio,
                      typeList=self.WEB_VIEW_HEIGHT_RATIOS)
        if messengerExtensions:
            self._messengerExtensions: bool = True
            sets.if_exists(self, '_fallbackUrl', fallbackUrl)

        if not webviewShareButton:
            self._webviewShareButton: str = 'hide'

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {}
            self._button['type'] = self.buttonType
            self._button['title'] = getattr(self, '_title')
            self._button['url'] = getattr(self, '_url')
            if self._messengerExtensions:
                self._button['messenger_extensions'] = \
                    self._messengerExtensions
                self._button['fallback_url'] = \
                    getattr(self, '_fallbackUrl')
            if hasattr(self, '_webviewHeightRatio'):
                self._button['webview_height_ratio'] = \
                    getattr(self, '_webviewHeightRatio')
            if hasattr(self, '_webviewShareButton'):
                self._button['webview_share_button'] = \
                    self._webviewShareButton
        return self._button


# DONE
class PostbackButton(Button):
    """Builds a postback button to be nested in a message."""

    def __init__(self, text: str, postbackData: str) -> None:
        self.buttonType: str = 'postback'
        sets.with_max_string_len(self, '_title', text,
                                 maxLen=self.BUTTON_TITLE_CHAR_LIMIT)
        self._payload: str = postbackData

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {
                'type': 'postback',
                'title': getattr(self, '_title'),
                'payload': self._payload}
        return self._button


# DONE
class ShareButton(Button):
    """Builds a share button that """

    def __init__(self, template=None) -> None:
        self.buttonType = 'element_share'
        if template:
            from .response_attachment import (ShareTemplate)
            if not isinstance(template, ShareTemplate):
                raise ValueError(
                    "Must pass in a ShareTemplate into ShareButton template")
            if self._shareTemplate.templateType != 'generic':
                raise ValueError("Share button template must be generic")

            self._shareTemplate = template

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {}
            self._button['type'] = self.buttonType
            if hasattr(self, '_shareTemplate'):
                self._button['share_contents'] = {
                    'attachment': self._shareTemplate.build()}
        return self._button


# DONE
class CallButton(Button):
    def __init__(self, text: str, phoneNumber: str) -> None:
        """
        Create a button that calls the phone number provided. This
            function doesn't validifiy the given phone number.
        NOTE: phoneNumber must contain a '+' followed by a valid
            country code.
        """
        self.buttonType: str = 'phone_number'
        sets.with_max_string_len(self, '_title', text,
                                 maxLen=self.BUTTON_TITLE_CHAR_LIMIT)
        sets.if_starts_with(self, '_payload', phoneNumber, prefix='+')

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {
                'type': self.buttonType,
                'title': getattr(self, '_title'),
                'payload': getattr(self, '_payload')}
        return self._button
