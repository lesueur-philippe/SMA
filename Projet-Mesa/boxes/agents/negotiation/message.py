from dataclasses import dataclass
from typing import Any

from .statuses import Status


@dataclass
class Message :
    """
    Simple class to describe messages between agents.
    """

    status  : Status
    """
    The status of the message. Statuses are defined in boxes.agents.negotiation.statuses
    """

    message : str = None
    """
    The content of the message
    """

    source : Any = None
    target : Any = None

    def __str__(self) :
        return f"\tStatus  : {self.status}\n" \
               f"\tMessage : {self.message}\n" \
               f"\tFrom    : {self.source}\n" \
               f"\tTo      : {self.target}"
