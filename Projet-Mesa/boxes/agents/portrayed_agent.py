from mesa import Agent, Model
from typing import Dict, Union

from abc import ABC, abstractmethod


class PortrayedAgent(Agent, ABC) :

    def __init__(self,
                 unique_id: int,
                 model: Model) :
        super(PortrayedAgent, self).__init__(unique_id, model)

    @abstractmethod
    def portray(self) -> Dict[str, Union[str, float]] :
        pass

