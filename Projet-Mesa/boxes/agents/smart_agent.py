import numpy as np
import random
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
        self.negociated = False
        self.negociated_with = []
        self.wished_positions = []
        self.round = 0
    
    def get_wished_positions(self):
        if not self.carrying :
            target_position = self.target_pos
        else :
            target_position = self.model.platform_pos
        if not target_position is None:
        # Get distance from each neighbour to target
            distances = [(cell, get_distance(target_position, cell)) for cell in neighbouring_cells]
            distance_from_current = get_distance(target_position, self.pos)
            wished = []
            for distance in distances:
                if distance[1] < distance_from_current :
                    wished.append(distance[0])
            return wished
        else :
            return self.wished_positions

    def __choose_action(self) -> None :

        if not self.negociated:
            self.available_next_steps()
        
        wished = self.get_wished_positions()

        agents = []
        for pos in self.wished_positions:
            cellmates = self.model.grid.get_cell_list_contents(self.model.grid.get_neighborhood(
                    pos, moore = False, include_center = True))
            for agent in cellmates:
                if isinstance(agent, SmartAgent) and (not agent == self) and not (agent in agents):
                    agents.append(agent)
        for agent in agents:
            if not (agent in self.negociated_with):
                self.__negociate(self, agent, wished)

    def __negociate(self, agent, wished_positions) -> Position :
        if not agent.negociated and agent.round == self.round:
            agent.available_next_steps()
        agent_wished_positions = agent..get_wished_positions()
        if len(agent_wished_positions) > 1:
            pos = random.choice(wished_positions)
            if pos in agent.wished_positions:
                agent.wished_positions.remove(pos)
            return pos
        elif len(agent_wished_positions) == 1:
            if agent.wished_positions > 1:
                for pos in wished_positions:
                    if not pos in agent_wished_positions:
                        try:
                            agent.wished_positions.remove(pos)
                        except ValueError:
                            pass
                    return pos
                pos = random.choice(wished_positions)
                try:
                    agent.wished_positions.remove(pos)
                except ValueError:
                    pass
                return pos
            elif len(agent.wished_positions) == 1:
                if wished_positions[0] == agent_wished_positions[0]:
                    pass
                else:
                    try:
                        agent.wished_positions.remove(wished_positions[0])
                    except ValueError:
                        pass
                    return wished_positions[0]
            else:
                
        else:

        
            

    def available_next_steps(self):
        neighbouring_cells = self.model.grid.get_neighborhood(
                self.pos, moore = False, include_center = False
        )
        for cell in neighbouring_cells.copy():
            cellmates = self.model.grid.get_cell_list_contents(cell)
            if len(cellmates) == 1:
                if isinstance(cellmates[0], Box) or (isinstance(cellmates[0], SmartAgent) and cellmates[0].round != self.round):
                    neighbouring_cells.remove(cell)
        self.wished_positions = neighbouring_cells
        
        
            

    def _pickup_box(self, box : Box) -> None :
        super(SmartAgent, self)._pickup_box(box)
        print("Pickup !")
        self.target_box = self.model.platform
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
        bs = self.__negociate()
        # print(f"BS : {bs}")
        self.model.grid.move_agent(self, bs)
        # print(self.pos)

    def assign_box(self, box : Box) :
        self.target_box = box
        self.target_pos = box.pos

    def step(self) -> None :
        # print("Step !", self)
        # attribute
        print(f"Positions souhaitées : {self.wished_positions}, a négocié : {self.negociated}")
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
        else:
            self._move()
        self.negociated_with = []
        self.negociated = False
        self.round +=1
