from enum import Enum


class Status(Enum) :
    """
    Different statuses for agent messages.
    """

    ASK     = 0
    AGREE   = 1
    REFUSE  = 2
    DISCUSS = 3
    CONFIRM = 4
    RETRACT = 5
