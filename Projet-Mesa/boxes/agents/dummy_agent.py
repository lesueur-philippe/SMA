from abc import ABC

from .templates import BaseAgent
from mesa import Model

from .props import Box


class DummyAgent(BaseAgent, ABC) :
    """
    A class for a dummy agent.

    The dummy agent moves randomly until he finds a box then returns to the destination cell.
    He does not communicate with his fellow agents at all.
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
        super(DummyAgent, self).__init__(unique_id, model, **kwargs)

    def _move(self) -> None :
        """
        Lets the agent move in the neighbouring cells. Cell is chosen at random if the agent
        is not carrying, if he is, the cell is the cell closest to the destination.
        """
        possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore = True, include_center = False
        )
        if self.carrying :
            new_position = min(possible_steps)
        else :
            new_position = self.random.choice(possible_steps)

        print(self.pos)
        self.model.grid.move_agent(self, new_position)
        print(self.pos)

    def step(self) -> None :
        print("Moving")
        self._move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        boxes = [agent for agent in cellmates if isinstance(agent, Box)]
        # print(boxes)
        if len(boxes) > 0 :
            self._pickup_box(boxes[0])

        if self.pos == (0, 0) :
            self._drop_box()

