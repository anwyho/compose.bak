from compose.process.controller import (Controller)
from compose.send.response_builder import (ResponseBuilder)


class BartbotController(Controller):
    """
    Calling produce_responses from this class sends an echo of the
        received message.
    """

    def process_message(self) -> ResponseBuilder:
        return ResponseBuilder(
            recipientId=self.message.senderId,
            text=f"You typed {self.message.text if hasattr(self.message, 'text') else '[no text found]'}",  # noqa: E501
            description="Message echo from EchoController")


CONTROLLER = BartbotController