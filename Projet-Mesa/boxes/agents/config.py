from enum import Enum


class AgentDefaults(Enum) :
    """
    Default configuration values for Agent classes
    """

    BASE_STRENGTH = 10


class BoxDefaults(Enum) :
    """
    Default configuration values for Box Classes
    """
    BASE_WEIGHT = 10
    NOISE_WEIGHT = False
