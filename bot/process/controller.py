import boto3  # noqa
import json  # noqa
import logging  # noqa
import time  # noqa

from typing import (Dict, List, Optional, Tuple, Union)  # noqa

import compose.recv as recv
# import compose.send as send
from compose.process import (Controller)
from compose.send import (button, response, response_attachment, ResponseBuilder)  # noqa
from compose.utils.requests import get

from bot.resources.map import (yield_map_id)
from bot.phrasing import (Phrase)

from .entity import (BartbotEntityParser)
from .user import (BartbotUser)

DRY_RUN = False


class BartbotController(Controller):

    def __init__(self, message, dryRun: bool = False) -> None:

        super().__init__(message=message, dryRun=dryRun)
        self.user: BartbotUser = BartbotUser(id=message.senderId)
        self.phrase: Phrase = Phrase(initialLocale=self.user.locale)
        self._dryRun: bool = DRY_RUN

    # ## PRE- & POST- PROCESSING ## #

    # OVERRIDES CONTROLLER
    def preprocess_message(self):
        self.send_seen_and_typing_on_indicators()
        self.futureEntities = self._executor.submit(self.get_wit_entities) \
            if hasattr(self.message, 'text') else {}

    # OVERRIDES CONTROLLER
    def postprocess_message(self):
        self.send_typing_off_indicator()

    # ## Pre- and Post-Processing Helpers ## #

    def send_seen_and_typing_on_indicators(self):
        seenResponse = ResponseBuilder(
            recipientId=self.message.senderId,
            senderAction="mark_seen",
            description="Marking message as seen",
            dryRun=self._dryRun)
        seenResponse.next_chain(
            senderAction="typing_on",
            description="Turning typing on")
        self._executor.submit(seenResponse.send())

    def send_typing_off_indicator(self):
        typingOffResponse = ResponseBuilder(
            recipientId=self.message.senderId,
            senderAction="typing_off",
            description="Turning typing off",
            dryRun=self._dryRun)
        self._executor.submit(typingOffResponse.send())

    def send_waiting_response(self, respTail: ResponseBuilder):
        respBranch = respTail.branch(
            text=self.phrase.get('wait'),
            description="Wait text")
        respBranch.next_chain(
            senderAction="typing_on",
            description="Turning typing on for waiting")
        self._executor.submit(respBranch.send)

    def get_wit_entities(self):
        return BartbotEntityParser(
            text=self.message.text,
            senderId=self.message.senderId)

    # ## PROCESS MESSAGE ## #

    def process_message(self):
        self.phrase.add_attributes(
            firstName=self.user.fn)

        head = respTail = ResponseBuilder(
            recipientId=self.message.senderId,
            dryRun=self._dryRun)

        if isinstance(self.message, recv.Attachment):
            respTail = self.process_attachment(respTail)

        elif isinstance(self.message, recv.Postback):
            respTail = self.process_postback(respTail)

        # BUG: Figure out why I can't call Text as `Text`
        elif isinstance(self.message, recv.Text):
            respTail = self.process_text(respTail)

        return head

    def process_attachment(self, respTail) -> ResponseBuilder:
        respTail.text = self.phrase.get(
            'attachment', useName=True)
        respTail.description = "Attachment response"
        return respTail

    def process_postback(self, respTail) -> ResponseBuilder:
        if self.message.payload == 'map':
            respTail = self.map_response(respTail)
        return respTail

    def process_text(self, respTail) -> ResponseBuilder:
        self.entities = self.await_entities()

        respTail.text = f'You typed: "{self.message.text}"'
        respTail.description = "Echoing message"
        respTail = respTail.next_chain()

        if not hasattr(self.entities, 'entities'):
            respTail = self.no_nlp_response(respTail)
        else:
            # Debugging text
            respTail.text = str(self.entities)
            respTail.description = "Wit self.entities"
            respTail = respTail.next_chain()
            try:
                respTail = self.process_intent(self.entities.intent, respTail)
            except Exception as e:
                respTail = self.error_response(respTail, e)

    def process_intent(self, intent: str, respTail: ResponseBuilder) \
            -> ResponseBuilder:
        if 'help' == intent:
            respTail = self.help_response(respTail)
        elif 'map' == intent:
            respTail = self.map_response(respTail)
        elif 'travel' == intent:
            respTail = self.travel_response(respTail)
        elif 'single-trip-cost' == intent:
            respTail = self.cost_response(respTail)
        elif 'round-trip-cost' == intent:
            respTail = self.cost_response(
                respTail, roundTrip=True)
        elif 'weather' == intent:
            respTail = self.weather_response(respTail)
        elif 'reset' == intent:
            respTail = self.reset_response(respTail)
        else:
            respTail = self.unknown_response(respTail)

        # TODO: self.add_quick_replies
        respTail.add_quick_reply(
            text="What is love?", postbackPayload="Payload")
        respTail.add_quick_reply(
            text="Baby don't hurt me...", postbackPayload="Payload")
        respTail.add_quick_reply(
            text="Baby don't hurt me...", postbackPayload="Payload")
        respTail.add_quick_reply(
            text="No more...!", postbackPayload="Payload")

        return respTail

    def await_entities(self) -> dict:
        while not self.futureEntities.done():
            pass
        return self.futureEntities.result()

    # ## Specific Response Helpers ## #

    def help_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.text = self.phrase.get('helpText')
        respTail.description = "Help text response"
        return respTail

    def map_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.text = self.phrase.get('delivery')
        respTail.description = "Delivery text"
        # respTail = respTail.next_chain(
        #     text=self.phrase.get('delivery'),
        #     description="Delivery text")
        mapIdGen = yield_map_id()
        mapId = next(mapIdGen)
        if not mapId:
            self.send_waiting_response(respTail)
            mapId = next(mapIdGen)
        if mapId:
            respTail = respTail.next_chain(
                attachment=response_attachment.Asset(
                    assetType='image', attchId=mapId),
                description="Map asset from attachment ID")
        else:
            # TODO: Backup plan
            pass

        return respTail

    def cost_response(self, respTail: ResponseBuilder,
                      roundTrip: bool = False) -> ResponseBuilder:
        respTail.text = "[TODO: Fill in the cost response.]"
        respTail.description = "Cost text"
        return respTail

    def travel_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.text = "[TODO: Fill in the travel response.]"
        respTail.description = "Travel text"

        # TODO: Outsource this to new file

        # HACK: Just trying to get basic functionality

        from bot.utils.keys import BART_PUBL

        params: dict = {
            'cmd': 'depart' if self.entities.timeArr is None else 'arrive',
            'orig': self.entities.stn,
            'dest': self.entities.stnDest,
            # 'time': time.strftime("%-I:%M %p", self.entities.time if self.entities.timeArr is None else self.entities.timeArr),  # noqa: E501
            'b': '1',
            'a': '4',
            'json': 'y',
            'key': BART_PUBL
        }

        ok, resp = get(
            url="http://api.bart.gov/api/sched.aspx", params=params)

        trips: list = resp['root']['schedule']['request']['trip']
        strTrips: list = []
        for trip in trips:
            strTrips.append(f"{trip['@origin']} {trip['@origTimeMin']} to {trip['@destination']} {trip['@destTimeMin']}")  # noqa: E501
        respTail = respTail.next_chain(
            text='\n'.join(strTrips),
            description='HACK trip info')

        return respTail

    def weather_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.text = "[TODO: Fill in the weather response.]"
        respTail.description = "Weather text"
        return respTail

    def reset_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.text = "[TODO: Fill in the reset response.]"
        respTail.description = "Reset text"
        return respTail

    def unknown_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.text = "[TODO: Fill in the unknown text response.]"
        respTail.description = "Unknown text"
        return respTail

    def no_nlp_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.text = "Sorry, I seem to have lost my NLP... Try asking me that later!"  # noqa
        respTail.description = "No NLP available."
        return respTail

    def error_response(self, respTail: ResponseBuilder, err) \
            -> ResponseBuilder:
        respTail.text = f"Oops! Something went wrong. Sorry about that...\n\nDebugging info: {err}"  # noqa: E501
        respTail.description = f"ERROR: {err}"
        return respTail
