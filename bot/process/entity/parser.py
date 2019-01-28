import json  # noqa
import logging
import time

from datetime import (datetime)  # noqa
from typing import(Dict, Optional)  # noqa

from compose.process.abstract_parser import (AbstractWitParser, WitParsingError)  # noqa


def get_datetime(witTime: str):
    print(f"witTime: {witTime}")
    dt = witTime[:19] + witTime[23:26] + witTime[27:]
    return time.strptime(dt, "%Y-%m-%dT%H:%M:%S%z") if witTime else None


class BartbotEntityParser(AbstractWitParser):

    # Calculated from F1 Score from Wit Model.
    # Source:
    #   https://towardsdatascience.com/beyond-accuracy-precision-and-recall-3da06bea9f6c
    # Calculation: https://www.desmos.com/calculator/ectgpnxult
    MIN_CONFIDENCE = 0.54

    def __repr__(self):
        return f"""{self.intent} - Intent\n{self.stn} - Station (Arr)\n{self.stnDest} - Station (Dest)\n{self.time} - Time (Dep)\n{self.timeArr} - Time (Arr)\n{self.decision} - Decision?\n{self.greetings} - Greeting?\n{self.thanks} - Thanks?\n{self.bye} - Salutation?"""  # noqa

    def parse_entities(self):
        # print(json.dumps(self.entities, indent=2))

        # Attributes of Bartbot NLP
        self.intent: Optional[str] = None
        self.stn: Optional[str] = None
        self.stnDest: Optional[str] = None
        self.time: Optional[str] = None
        self.timeArr: Optional[str] = None
        self.decision: Optional[str] = None

        self.greetings: bool = False
        self.thanks: bool = False
        self.bye: bool = False

        # Metavariables
        self.confirmTime = False

        entities = self.entities
        # Handle datetime entity
        if 'datetime' in entities or \
                'dep' in entities or \
                'arr' in entities:

            if 'dep' in entities:
                dep = entities['dep'][0]
                self.time = get_datetime(
                    self.ret_val_if_confident(dep))
            if 'arr' in entities:
                arr = entities['arr'][0]
                self.timeArr = get_datetime(
                    self.ret_val_if_confident(arr))
            if 'datetime' in entities:
                witDatetime = entities['datetime'][0]
                if self.time is None:
                    self.time = 'datetime'
                elif self.timeArr is None:
                    self.timeArr = 'datetime'
                elif witDatetime.get('type') == 'interval':
                    self.time = 'datetime'
                    self.timeArr = 'datetime'

        self.confirmTime = True

        # if 'datetime' in entities or \
        #     'dep' in entities or \
        #         'arr' in entities:

        #     witDatetime = entities['datetime'][0]
        #     if 'value' == witDatetime.get('type'):
        #         self.time = get_datetime(
        #             self.ret_val_if_confident(witDatetime))
        #     elif 'interval' == witDatetime.get('type') and \
        #             self.ret_val_if_confident(witDatetime, key='to'):
        #         self.time = get_datetime(witDatetime['from']['value'])
        #         self.timeArr = get_datetime(witDatetime['to']['value'])

        # Handle station entities
        if 'orig' in entities:
            self.stn = self.ret_val_if_confident(entities['orig'])
        if 'dest' in entities:
            self.stnDest = self.ret_val_if_confident(entities['dest'])
        if 'station' in entities:
            if self.stn is None:
                self.stn = self.ret_val_if_confident(entities['station'])
            elif self.stnDest is None:
                self.stnDest = self.ret_val_if_confident(entities['station'])
            else:
                logging.warning("We got three stations.")

        # Handle intents
        if 'intent' in entities:
            self.intent = self.ret_val_if_confident(entities['intent'])

        # Handle thanks
        thanks = self.ret_val_if_confident(entities.get('thanks'))
        if thanks is not None:
            self.thanks = True if thanks == 'true' else False

        # Handle greetings
        greetings = self.ret_val_if_confident(entities.get('greetings'))
        if greetings is not None:
            self.greetings = True if greetings == 'true' else False

        # Handle bye
        bye = self.ret_val_if_confident(entities.get('bye'))
        if bye is not None:
            self.bye = True if bye == 'true' else False

        # Handle decision
        if 'decision' in entities:
            self.decision = self.ret_val_if_confident(entities['decision'])

        self.handle_model_bugs()

    def handle_model_bugs(self):
        # TODO: The NLP model always recognizes "fremont" as WARM
        pass

    def ret_val_if_confident(self,
                             entity: dict,
                             minConfidence: float = -1,
                             key: str = 'value'):
        """
        Get the value of a Wit entity if it is above a minimum
            confidence threshold.
        """
        if minConfidence == -1:
            minConfidence = self.MIN_CONFIDENCE
        if isinstance(entity, list) and len(entity):
            entity = entity[0]
        return entity[key] if isinstance(entity, dict) and \
            entity.get('confidence', 0) > minConfidence else None


# "arr": [
#     {
#         "confidence": 0.92679818449293,
#         "values": [
#             {
#                 "value": "2018-11-24T20:00:00.000-08:00",
#                 "grain": "hour",
#                 "type": "value"
#             },
#             {
#                 "value": "2018-11-25T20:00:00.000-08:00",
#                 "grain": "hour",
#                 "type": "value"
#             },
#             {
#                 "value": "2018-11-26T20:00:00.000-08:00",
#                 "grain": "hour",
#                 "type": "value"
#             }
#         ],
#         "value": "2018-11-24T20:00:00.000-08:00",
#         "grain": "hour",
#         "type": "value"
#     }
# ],
