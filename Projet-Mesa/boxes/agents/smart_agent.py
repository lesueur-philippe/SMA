import numpy as np

from .base_agent import BaseAgent
from mesa import Model

from .props import Box, Destination

from ..utils.types import Position
from ..utils import get_distance


class SmartAgent(BaseAgent) :
    
    def __init__(self,
                 unique_id : int,
                 model : Model,
                 **kwargs : float) :
        super(SmartAgent, self).__init__(unique_id, model, **kwargs)

        self.target_box : Box = None
        self.target_pos : Position = None
        # self.next_steps : List[Tuple[int, int]] = []
        self.carried_box : Box = None

    def _choose_action(self) -> None :
        pass

    def __best_next_step(self) -> Position :

        if self.target_box is None :
            return self.pos
        else :
            neighbouring_cells = self.model.grid.get_neighborhood(
                    self.pos, moore = False, include_center = True
            )

            if not self.carrying :
                target_position = self.target_pos
            else :
                target_position = self.model.platform_pos

            # Get distance from each neighbour to target
            distances = [(cell, get_distance(target_position, cell)) for cell in neighbouring_cells]
            distances = sorted(distances, key = lambda el : el[1])
            best      = distances[0]
            distance_from_current = get_distance(target_position, self.pos)
            # print(distances)
            if best[1] < distance_from_current :
                return best[0]
            else :
                return self.pos

    def _pickup_box(self, box : Box) -> None :
        super(SmartAgent, self)._pickup_box(box)
        print("Pickup !")
        self.target_pos = self.model.platform_pos
        self.carried_box = box
        print(self.carrying, self.currently_carrying, self.target_pos, self.target_box)

    def _drop_box(self) -> None :
        super(SmartAgent, self)._drop_box()
        self.carried_box = None
        self.target_pos  = None
        self.target_box  = None

    def _move(self) -> None :
        # print("Move !", self)
        # print(self.pos)
        bs = self.__best_next_step()
        # print(f"BS : {bs}")
        self.model.grid.move_agent(self, bs)
        # print(self.pos)

    def assign_box(self, box : Box) :
        self.target_box = box
        self.target_pos = box.pos

    def step(self) -> None :
        # print("Step !", self)
        # Move
        self._move()

        # Act on neighbours
        neighbours = self.model.grid.get_neighborhood(
                self.pos, moore = False, include_center = False
        )
        close_agents = self.model.grid.get_cell_list_contents(neighbours)

        print(f"{neighbours}\n{self.target_pos}")
        if not self.carrying and self.target_pos in neighbours :
            print("Case 1")
            self._pickup_box(self.target_box)
        elif self.carrying and self.model.platform_pos in neighbours :
            print("Case 2")
            self._drop_box()
