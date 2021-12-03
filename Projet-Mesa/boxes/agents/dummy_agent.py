from abc import ABC
from typing import Dict, Union

from .base_agent import BaseAgent
from mesa import Model

from .props.boxes import Box


class DummyAgent(BaseAgent, ABC) :

    def __init__(self,
                 unique_id : int,
                 model : Model,
                 **kwargs : int) :
        super(DummyAgent, self).__init__(unique_id, model, **kwargs)

    def _choose_action(self) :
        print("Moving")
        self.__move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        boxes = [agent for agent in cellmates if isinstance(agent, Box)]
        # print(boxes)
        if len(boxes) > 0 :
            self._pickup_box(boxes[0])

        if self.pos == (0, 0) :
            self._drop_box()

    def __move(self) :
        possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore = True, include_center = False
        )
        if self.carrying :
            new_position = min(possible_steps)
        else :
            new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

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
