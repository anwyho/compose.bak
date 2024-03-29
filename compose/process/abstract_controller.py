import logging  # noqa
import sys

from abc import (ABC, abstractmethod)
from concurrent.futures import (ThreadPoolExecutor)
from typing import (Optional)

from compose.send import (ResponseBuilderError, ResponseBuilder)
from compose.send.response import (InvalidResponseStructureError, Response)
from compose.utils.errors import (gen_err_msg)


class AbstractController(ABC):
    def __init__(self, message, dryRun: bool = False) -> None:
        self.message = message
        self._dryRun: bool = dryRun
        self._executor: Optional[ThreadPoolExecutor] = None

    def produce_responses(self) -> ResponseBuilder:
        """
        Lay out overall logic of Controller and expose all processing
            functions to a thread executor
        """

        try:
            response: Optional[Response] = None
            with ThreadPoolExecutor(max_workers=8) as executor:
                self._executor = executor

                self.preprocess_message()
                response = self.process_message()
                self.postprocess_message()

        except (InvalidResponseStructureError, ResponseBuilderError) as e:
            gen_err_msg(sys.exc_info(), e)
        except Exception as e:
            gen_err_msg(sys.exc_info(), e)

        finally:
            # TODO: What happens if a Response is not generated?
            if not isinstance(response, ResponseBuilder):
                response = Response(apiUrl='', dryRun=True,
                                    description='No valid response was generated.')  # noqa: E501
            self._executor = None

        return response

    @abstractmethod
    def process_message(self) -> Response:
        """
        Parse the message and generate a response to send using the
            ResponseBuilder.
        """
        pass

    def preprocess_message(self) -> None:
        pass

    def postprocess_message(self) -> None:
        pass


class EchoController(AbstractController):
    """
    Calling produce_responses from this class sends an echo of the
        received message.
    """

    def process_message(self) -> ResponseBuilder:
        return ResponseBuilder(
            recipientId=self.message.senderId,
            text=f"You typed {self.message.text if hasattr(self.message, 'text') else '[no text found]'}",  # noqa: E501
            description="Message echo from EchoController")
