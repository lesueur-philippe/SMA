from abc import ABC, abstractmethod

from mesa import Model

from .config import AgentDefaults
from .portrayed_agent import PortrayedAgent
from .props.boxes import Box


class BaseAgent(PortrayedAgent, ABC) :
    
    def __init__(self, 
                 unique_id : int,
                 model : Model,
                 **kwargs : int) :
        
        super(BaseAgent, self).__init__(unique_id, model)
        self.carrying = False
        self.strength = kwargs.get("strength", AgentDefaults.BASE_STRENGTH.value)
        self.currently_carrying = 0

    @abstractmethod
    def _choose_action(self) :
        pass

    def _pickup_box(self, box : Box) :

        self.carrying = True
        self.currently_carrying += box.weight

        del self.model.boxes[box.unique_id]
        self.model.schedule.remove(box)
        self.model.grid.remove_agent(box)

    def _drop_box(self) :
        print(f"Agent dropped box of weight {self.currently_carrying}")
        self.carrying = False
        self.currently_carrying = 0

    def step(self) -> None :
        print(f"Step called {self}")
        print(f"{self.pos}")

        self._choose_action()
        
