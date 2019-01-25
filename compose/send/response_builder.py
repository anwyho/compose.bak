import json  # noqa
import logging
import wrapt

from typing import (List, Optional, Union)

from compose.utils.urls import (MESSAGES_API)

from .response_attachment import (ResponseAttachment)
# from .button import (Button)
from .response import (Response)


@wrapt.decorator
def require_rebuild(wrapped, instance, args, kwargs):
    """
    Setter wrapper that resets the built tag to `False`.
    """
    inst = instance if instance else(
        args[0] if isinstance(args[0], Response) else None)
    if inst:
        inst._built, inst._passingChecks, inst._modified = False, False, True
    return wrapped(*args, **kwargs)


class ResponseBuilderError(Exception):
    pass


# Interface for Send API
class ResponseBuilder(Response):
    """Provides an interface for sending to Send API"""

    def __init__(self,
                 apiUrl: Optional[str] = MESSAGES_API,
                 dryRun: bool = False,
                 description: Optional[str] = None,
                 attachment: Optional[ResponseAttachment] = None,
                 messagingType: str = 'RESPONSE',
                 metadata: str = '',
                 notificationType: str = '',
                 tag: str = '',
                 text: str = '',
                 timeout: float = 0,
                 senderAction: str = '',
                 **recipientArgs) -> None:
        super(ResponseBuilder, self).__init__(apiUrl=apiUrl,
                                              description=description,
                                              dryRun=dryRun,
                                              timeout=timeout)

        self.attachment: Optional[ResponseAttachment] = attachment
        self.messagingType: str = messagingType
        self.metadata: str = metadata
        self.notificationType: str = notificationType
        self.tag: str = tag
        self.text: str = text
        self.senderAction: str = senderAction
        if recipientArgs:
            self.set_recipient(**recipientArgs)
        self.quickReplies: List[dict] = []
        self._built: bool = False
        self._modified: bool = False

    def build(self):
        """
        Construct JSON for Messenger Platform Send API. This is
            adapter for Messenger.
        """
        if self._built:
            return

        self._data: dict = {}

        self._data['messaging_type'] = self.messagingType
        self._data['recipient'] = self.recipient()

        if self.text or self.attachment:
            # Chained response contains quick replies but is empty,
            #   so delete chained response and move quick replies to
            #   current message
            if getattr(self._chainedResponse, 'quickReplies', None) and \
                    not getattr(self._chainedResponse, 'attachment', None) and\
                    not getattr(self._chainedResponse, 'text', None):
                self.quickReplies = self._chainedResponse.quickReplies
                self._chainedResponse = None

            # Prep message
            message: dict = {}
            if self.metadata:
                message['metadata'] = self.metadata
            if self.quickReplies:
                message['quick_replies'] = self.quickReplies

            if self.text:
                message['text'] = str(self.text)
            elif self.attachment:
                message['attachment'] = self.attachment.build()
            else:
                raise ResponseBuilderError(
                    "Expected either text or attachment.")

            # Prep response
            self._data['message'] = message
            self._data['notification_type'] = self.notificationType
            if self.tag:
                self._data['tag'] = self.tag

        elif self.senderAction is not None:
            self._data['sender_action'] = self.senderAction

        self._built = True

    def send(self, inChain: bool = False) -> bool:
        """
        Verify that response data is built before calling super send
            method.
        """
        if not self._built:
            self.build()
        return super(ResponseBuilder, self).send(inChain=inChain)

    # DUPLICATE RESPONSES #

    def next_chain(self, **builderInitKwargs):
        """
        Create and attach a chained response and set recipient
            and moves quick replies.
        """
        # TODO: Make some sort of check for this?
        # if not self._modified:
        #     return self
        self._chainedResponse = ResponseBuilder(**builderInitKwargs)
        self._chainedResponse._dryRun = self._dryRun
        self._chainedResponse._recipient = self._recipient
        self._chainedResponse.quickReplies = self.quickReplies
        self.quickReplies = []
        return self._chainedResponse

    def branch(self, **builderInitKwargs):
        """Create a new response set the same recipient."""
        resp = ResponseBuilder(**builderInitKwargs)
        resp._dryRun = self._dryRun
        resp._recipient = self._recipient
        return resp

    # PROPERTIES #

    @require_rebuild
    def add_quick_reply(self,
                        contentType: str = 'text',
                        text: str = '',
                        postbackPayload: Union[str, int] = '',
                        imageUrl: str = '') -> dict:
        """
        Add a quick-reply to the message payload. Remove quick-reply
            not implemented yet.
        """

        if len(self.quickReplies) >= self.MAX_QUICK_REPLIES:
            raise ResponseBuilderError(
                f"Only {self.MAX_QUICK_REPLIES} quick replies are allowed per response.")  # noqa: E501
        contentType = contentType.lower()
        if contentType not in self.QUICK_REPLY_TYPES:
            raise ResponseBuilderError(
                "Attempted to create unsupported quick reply type.")

        quickReply: dict = {'content_type': contentType}
        if contentType == 'text':
            quickReply['title'] = text
            quickReply['payload'] = postbackPayload
            # HACK: These two lines are slightly clever. Consider refactoring.
            if imageUrl or text == '':
                if not imageUrl:
                    raise ResponseBuilderError(
                        "Expected image URL with empty title string.")
                quickReply['image_url'] = imageUrl

        self.quickReplies.append(quickReply)

    @property
    def attachment(self):
        return self._attachment

    @attachment.setter
    @require_rebuild
    def attachment(self, templateOrAsset: Optional[ResponseAttachment]):
        if templateOrAsset is not None and \
                not isinstance(templateOrAsset, ResponseAttachment):
            ResponseBuilderError(f"Attempted to set attachment to object other than Template, Asset, or None.")  # noqa: E501
        self._attachment = templateOrAsset

    @property
    def messagingType(self) -> str:
        return self._messagingType

    @messagingType.setter
    @require_rebuild
    def messagingType(self, messagingType: str) -> None:
        if messagingType not in self.MESSAGING_TYPES:
            ResponseBuilderError(f"Attempted to set messaging type to an unsupported messaging type {messagingType}.")  # noqa: E501
        self._messagingType = messagingType

    @property
    def metadata(self) -> str:
        return self._metadata

    @metadata.setter
    @require_rebuild
    def metadata(self, metadata: str) -> None:
        self._metadata = metadata

    @property
    def notificationType(self) -> str:
        return self._notificationType

    @notificationType.setter
    @require_rebuild
    def notificationType(self, notificationType: str) -> None:
        if notificationType not in self.NOTIFICATION_TYPES:
            ResponseBuilderError(f"Attempted to set notification type to an unsupported messaging type {notificationType}.")  # noqa: E501
        self._notificationType = notificationType

    def recipient(self) -> dict:
        return self._recipient

    @require_rebuild
    def set_recipient(self,
                      recipientId: Optional[str] = None,
                      phoneNumber: Optional[str] = None,
                      firstName: Optional[str] = None,
                      lastName: Optional[str] = None,
                      userRef: Optional[str] = None) -> None:
        """
        Set recipient information with Facebook ID taking priority,
            followed by phone number and then user referral.
        """

        if recipientId:
            self._recipient: dict = {'id': recipientId}
        elif phoneNumber:
            self._recipient: dict = {
                'id': phoneNumber, 'phone_number': phoneNumber}
            if firstName and lastName:
                self._recipient['name']: dict = {
                    'first_name': firstName, 'last_name': lastName}
        elif userRef:
            self._recipient: dict = {'id': userRef, 'user_ref': userRef}
        else:
            logging.debug(
                f"Failed to set recipient info. Variable dump: \nrecipientId: {recipientId}\nphoneNumber: {phoneNumber}\nfirstName: {firstName}\nlastName: {lastName}\nuserRef: {userRef}")   # noqa: E501
            raise ResponseBuilderError("Failed to set recipient information.")

    @property
    def senderAction(self) -> str:
        return self._senderAction

    @senderAction.setter
    @require_rebuild
    def senderAction(self, senderAction: str) -> None:
        if senderAction not in self.SENDER_ACTIONS:
            ResponseBuilderError(f"Attempted to set sender action to an unsupported sender action {senderAction}.")  # noqa: E501
        self._senderAction = senderAction

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    @require_rebuild
    def tag(self, tag: str) -> None:
        if tag not in self.TAGS:
            ResponseBuilderError(
                f"Attempted to set tag to an unsupported tag {tag}.")
        self._tag = tag

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = str(text)
