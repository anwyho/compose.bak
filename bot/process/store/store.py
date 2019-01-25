import wrapt

from typing import (List, Optional)  # noqa

from bot.process.entity import (BartbotEntityParser)
from bot.process.user import (BartbotUser)


@wrapt.decorator
def try_state_compute(wrapped, instance, args, kwargs):
    res = wrapped(*args, **kwargs)

    inst = instance if instance else(
        args[0] if isinstance(args[0], Store) else None)
    if inst and inst._entities and inst._user:
        inst.compute_state()

    return res


class Store:
    def __init__(self):
        self._entities: Optional[BartbotEntityParser] = None
        self._user: Optional[BartbotUser] = None
        self.state: dict = {}

    @try_state_compute
    @property
    def entities(self, entities: BartbotEntityParser) -> None:
        self._entities = entities

    @try_state_compute
    @property
    def user(self, user: BartbotUser) -> None:
        self._user = user

    def compute_state(self) -> None:
        self.state['times_recomputed'] = self.state['times_recomputed'] + 1 \
            if 'times_recomputed' in self.state else 1
