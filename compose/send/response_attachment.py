import functools
import json  # noqa
import logging

from abc import (ABC, abstractmethod)
from typing import (List, Optional, Union)

from .response_utils import (set_if_exists)
from .button import (Button, UrlButton)


class ResponseAttachment(ABC):

    @abstractmethod
    def build(self):
        raise NotImplementedError


class Asset(ResponseAttachment):

    ASSET_TYPES = ['image', 'audio', 'video', 'file']

    def __init__(self,
                 assetType: str,
                 assetUrl: Optional[str] = None,
                 isReusable: bool = False,
                 attchId: Optional[str] = None):

        if assetType not in self.ASSET_TYPES:
            ValueError(f"Asset type {assetType} not supported.")

        payload: dict = {}

        if attchId and attchId.isdigit():
            payload['attachment_id'] = attchId
        elif assetUrl:
            payload['url'] = assetUrl
            payload['is_reusable'] = isReusable
        else:
            ValueError(
                "Expected asset URL or attachment ID when creating Asset.")

        self._data = {'type': assetType, 'payload': payload}

    def build(self):
        return self._data


class Template(ResponseAttachment, ABC):

    TEMPLATE_TYPES: List[Optional[str]] = [
        'generic',
        'button',
        'list',
        'media',
        # 'receipt',  # not currently supported
        'share',
    ]

    @classmethod
    def make_template(cls, templateType: str, **kwargs):
        if templateType == 'generic':
            return GenericTemplate(**kwargs)
        elif templateType == 'button':
            return ButtonTemplate(**kwargs)
        elif templateType == 'list':
            return ListTemplate(**kwargs)
        elif templateType == 'media':
            return MediaTemplate(**kwargs)
        elif templateType == 'share':
            return ShareTemplate(**kwargs)
        else:
            logging.warning(
                f"Attempted to make unsupported template type {templateType}.")

    @abstractmethod
    def build(self) -> dict:
        """
        The implemented versions of this method builds each
            element recursively until a dict of dicts and strings is
            created.
        NOTE: Use this method as a starting place by calling
            `template: dict = super().build()` and return template.
        """
        return {
            'type': 'template',
        }


class GenericTemplate(Template):

    MAX_GENERIC_ELEMENTS = 10
    IMAGE_ASPECT_RATIOS = ['horizontal', 'square']

    class GenericElement:

        TITLE_CHAR_LIMIT = 80
        SUBTITLE_CHAR_LIMIT = 80
        MAX_BUTTONS = 3

        def __init__(self,
                     title: str,
                     subtitle: Optional[str] = None,
                     imageUrl: Optional[str] = None,
                     buttons: Optional[List[Button]] = None,
                     defaultActionUrl: Optional[str] = None,
                     webviewHeightRatio: Optional[str] = None,
                     webviewShareButton: Optional[str] = None,
                     messengerExtensions: bool = False,
                     fallbackUrl: Optional[str] = None) -> None:

            set_if_exists(self, '_title', title,
                          maxLen=self.TITLE_CHAR_LIMIT,
                          raiseOnFail=True)
            if subtitle:
                set_if_exists(self, '_subtitle', subtitle,
                              maxLen=self.SUBTITLE_CHAR_LIMIT)
            if imageUrl:
                self._imageUrl = imageUrl
            # Accepts same arguments as UrlButton except Title
            if defaultActionUrl:
                self._type = 'web_url'
                self._defaultActionUrl = defaultActionUrl
                set_if_exists(self, '_webviewHeightRatio', webviewHeightRatio)
                set_if_exists(self, '_webviewShareButton', webviewShareButton)
                if messengerExtensions:
                    self._messengerExtensions = True
                    set_if_exists(self, '_fallbackUrl', fallbackUrl)

            if isinstance(buttons, list):
                set_if_exists(self, '_buttons', buttons,
                              maxLen=self.MAX_BUTTONS)

        def build(self) -> dict:
            if not hasattr(self, '_element'):
                self._element: dict = {}
                self._element['title'] = getattr(self, '_title')
                if hasattr(self, '_subtitle'):
                    self._element['subtitle'] = getattr(self, '_subtitle')
                if hasattr(self, '_imageUrl'):
                    self._element['image_url'] = self._imageUrl

                if hasattr(self, '_defaultActionUrl'):
                    defaultAction: dict = {}
                    defaultAction['type'] = self._type
                    defaultAction['url'] = self._defaultActionUrl
                    if hasattr(self, '_webviewHeightRatio'):
                        defaultAction['webview_height_ratio'] = \
                            getattr(self, '_webviewHeightRatio')
                    if hasattr(self, '_webviewShareButton'):
                        defaultAction['webview_share_button'] = \
                            getattr(self, '_webviewShareButton')
                    if self._messengerExtensions:
                        defaultAction['messenger_extensions'] = \
                            self._messengerExtensions
                        if hasattr(self, '_fallbackUrl'):
                            defaultAction['fallback_url'] = \
                                getattr(self, '_fallbackUrl')
                    self._element['default_action'] = defaultAction

                if hasattr(self, '_buttons'):
                    self._element['buttons'] = \
                        [b.build() for b in getattr(self, '_buttons', [])]

            return self._element

    def __init__(self,
                 imageAspectRatio: str = 'horizontal',
                 shareable: bool = False):
        self.templateType: str = 'generic'
        imageAspectRatio = imageAspectRatio.lower()
        set_if_exists(self, '_imageAspectRatio', imageAspectRatio,
                      types=self.IMAGE_ASPECT_RATIOS)
        self._shareable = shareable
        self._elements: list = []  # TODO: Initialize elements

    def add_element(self, **elementArgs: Union[Optional[str], bool]) -> bool:
        if len(self._elements) > self.MAX_GENERIC_ELEMENTS:
            logging.warning(f"Attempted to add one too many elements to template. Max number of elements is {self.MAX_GENERIC_ELEMENTS}.")  # noqa: E501
            return False
        else:
            self._elements.append(self.GenericElement(**elementArgs))
            return True

    def build(self) -> dict:
        if not hasattr(self, '_template'):
            self._template: dict = super().build()
            payload: dict = {
                'template_type': self.templateType,
                'image_aspect_ratio': getattr(self, '_imageAspectRatio',
                                              'horizontal'),
                'elements': [e.build() for e in self._elements],
                'shareable': self._shareable}
            self._template['payload'] = payload
        return self._template


# DONE
class ButtonTemplate(Template):

    TEXT_CHAR_LIMIT = 640
    MIN_BUTTONS = 1
    MAX_BUTTONS = 3

    def __init__(self,
                 text: str,
                 buttons: List[Button],
                 shareable: bool = False):
        self.templateType: str = 'button'
        set_if_exists(self, '_text', text, maxLen=self.TEXT_CHAR_LIMIT)
        self._shareable = shareable

        # Check that buttons is a list
        if not isinstance(buttons, list):
            ValueError("The buttons argument in ButtonTemplate must be a list of Buttons.")  # noqa: E501
        # Check that there are buttons in buttons
        if not buttons:
            ValueError("There must be buttons in the buttons list argument of ButtonTemplate.")  # noqa: E501
        # Check for each button in buttons to be a Button
        if not functools.reduce(
                lambda a, b: isinstance(a, Button) and isinstance(b, Button),
                buttons[:self.MAX_BUTTONS]):
            ValueError("Every element passed in the buttons argument of ButtonTemplate must be a Button.")  # noqa: E501
        else:
            set_if_exists(self, '_buttons', buttons,
                          maxLen=self.MAX_BUTTONS, raiseOnFail=True)

    def build(self) -> dict:
        if not hasattr(self, '_template'):
            self._template: dict = super().build()
            self._template['payload'] = {
                'template_type': self.templateType,
                'text': getattr(self, '_text'),
                'buttons': [b.build() for b in getattr(self, '_buttons')],
                'shareable': self._shareable}
        return self._template


class ListTemplate(Template):

    TOP_ELEMENT_STYLES = ['compact', 'large']
    MIN_LIST_ELEMENTS = 2
    MAX_LIST_ELEMENTS = 4
    TITLE_CHAR_LIMIT = 80
    SUBTITLE_CHAR_LIMIT = 80
    MAX_BUTTONS = 1

    class ListElement():
        def __init__(self):
            pass

    def __init__(self,
                 topElementStyle: str = 'compact',
                 templateButton: Optional[Button] = None,
                 shareable: bool = False):
        self.templateType: str = 'list'
        set_if_exists(self, '_topElementStyle',
                      topElementStyle, types=self.TOP_ELEMENT_STYLES)
        set_if_exists(self, '_templateButton', templateButton)
        self._shareable = shareable
        self._elements: List[self.ListElement] = []

    def build(self) -> dict:
        if len(self._elements) < self.MIN_LIST_ELEMENTS:
            raise ValueError(
                f"Attempted to build List Template without {self.MIN_LIST_ELEMENTS} list elements. Please add {self.MIN_LIST_ELEMENTS-len(self._elements)} to {self.MAX_LIST_ELEMENTS-len(self._elements)} more list elements to build this template.")   # noqa: E501

        template: dict = super().build()

        payload: dict = {}
        payload['template_type'] = self.templateType
        if hasattr(self, '_topElementStyle'):
            payload['top_element_style'] = getattr(self, '_topElementStyle')
        if hasattr(self, '_templateButton'):
            payload['buttons'] = [getattr(self, '_templateButton')]
        payload['elements'] = [e.build() for e in self._elements]
        payload['shareable'] = self._shareable

        template['payload'] = payload

        return template


# DONE
class MediaTemplate(Template):

    MAX_MEDIA_ELEMENTS = 1
    MAX_BUTTONS = 1
    MEDIA_TYPES = ['image', 'video']

    # TODO: Make MediaTemplate
    def __init__(self,
                 mediaType: str,
                 attachmentId: Optional[str] = None,
                 url: Optional[str] = None,
                 button: Optional[Button] = None,
                 shareable: bool = False):
        # TODO: Include a NOTE about url receiving priority
        self.templateType: str = 'media'
        set_if_exists(self, '_mediaType', mediaType, types=self.MEDIA_TYPES)

        set_if_exists(self, '_url', url)
        if not hasattr(self, '_url'):
            if attachmentId and attachmentId.isdigit():
                self._attachmentId = attachmentId
            else:
                ValueError(f"Invalid attachment ID '{attachmentId}' provided for media template.")  # noqa: E501
            if not hasattr(self, '_attachmentId'):
                ValueError("Attempted to make a media template without any media source. Please include a valid attachment ID or URL.")  # noqa: E501
        set_if_exists(self, '_button', button)
        self._shareable = shareable

    def build(self) -> dict:
        template: dict = super().build()

        element: dict = {}
        element['media_type'] = getattr(self, '_mediaType')
        if hasattr(self, 'attachmentId'):
            element['attachment_id'] = self._attachmentId
        else:
            element['url'] = getattr(self, '_url')
        if hasattr(self, 'button'):
            # TODO: The below seems dangerous
            element['buttons'] = [getattr(self, '_button').build()]

        template['payload'] = {
            'template_type': self.templateType,
            'elements': [element],
            'shareable': self._shareable}

        return template

# DONE


class ShareTemplate(GenericTemplate):
    MAX_BUTTONS = 1
    MAX_GENERIC_ELEMENTS = 1  # TODO: Figure out if it needs to be limited

    def __init__(self,
                 urlButton: Optional[UrlButton] = None,
                 imageAspectRatio: Optional[str] = 'horizontal',
                 **genericElementArgs):
        super().__init__(
            buttons=[urlButton] if urlButton else [],
            imageAspectRatio=imageAspectRatio)
        super().add_element(buttons=[urlButton] if urlButton else [],
                            **genericElementArgs)

    def add_element(self, **elementArgs: Union[Optional[str], bool]):
        raise NotImplementedError("Adding more elements is not supported for making a new ShareTemplate.")  # noqa: E501

    def build(self) -> dict:
        return super().build()

