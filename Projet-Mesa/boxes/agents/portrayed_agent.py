from mesa import Agent, Model
from typing import Dict, Union

from abc import ABC, abstractmethod


class PortrayedAgent(Agent, ABC) :
    """
    Abstract class to represent a **MESA** agent that can be portrayed on a grid.

    Only proposes a portray method that must be implemented in order to represent
    the agent on a grid.
    """

    def __init__(self,
                 unique_id: int,
                 model: Model) :
        """
        Generates the agent

        :param unique_id: the id for the agent
        :param model: the model the agent is linked to
        """
        super(PortrayedAgent, self).__init__(unique_id, model)

    @abstractmethod
    def portray(self) -> Dict[str, Union[str, float]] :
        """
        Returns the definition for the depiction of the agent on the screen.

        The definition is returned as a map of all attributes needed to show the agent.

        :return: the map of attributes representing the agent
        """
        pass

