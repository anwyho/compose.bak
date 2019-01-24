from typing import (List)

from .controller import (Controller, EchoController)  # noqa


def import_controller():
    """
    This bot controller is wrapped in a function to avoid circular
        imports. NOTE: That was tricky to debug...
    """
    from bot import (CONTROLLER)
    return CONTROLLER


__all__: List[str] = ['Controller', 'import_controller']
