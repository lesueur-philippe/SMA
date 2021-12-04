from abc import ABC, abstractmethod
from typing import Dict, Union

from mesa import Model

from .config import AgentDefaults
from .portrayed_agent import PortrayedAgent
from .props.boxes import Box


class BaseAgent(PortrayedAgent, ABC) :
    """
    Abstract class to represent a *proper* agent, as in an agent capable
    of taking decisions.
    """
    
    def __init__(self, 
                 unique_id : int,
                 model : Model,
                 **kwargs : int) :
        """
        Generates the agent

        :param unique_id: the id for the agent
        :param model: the model the agent is related to
        :param kwargs: additional configuration values
        """
        
        super(BaseAgent, self).__init__(unique_id, model)
        self.carrying = False
        self.strength = kwargs.get("strength", AgentDefaults.BASE_STRENGTH.value)
        self.currently_carrying = 0

    def _pickup_box(self, box : Box) -> None :
        """
        Lets the agent pick up a given box

        Removes the box from the model.

        :param box: the box to pick up
        """

        # Update attributes
        self.carrying = True
        self.currently_carrying += box.weight

        # Remove box
        del self.model.boxes[box.unique_id]
        self.model.schedule.remove(box)
        self.model.grid.remove_agent(box)

    def _drop_box(self) -> None :
        """
        Lets the agent drop the box they are currently carrying
        """

        # print(f"Agent dropped box of weight {self.currently_carrying}")
        self.carrying = False
        self.currently_carrying = 0

    @abstractmethod
    def step(self) -> None :
        pass

    def portray(self) -> Dict[str, Union[str, float]] :
        portrayal = {
            "Shape"  : "rect",
            "Filled" : "true",
            "w"      : 0.8,
            "h"      : 0.8,
            "Layer"  : 0
        }
        if not self.carrying :
            color = "#A0B8CF"
        else :
            color = "#EFAD06"
        portrayal["Color"] = color

        return portrayal
        
