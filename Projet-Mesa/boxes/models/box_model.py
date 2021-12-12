from mesa import Model
from mesa.space import MultiGrid
from typing import List, Optional, Tuple

from boxes.agents import Box, Destination, PortrayedAgent


class BoxModel(Model) :

    def __init__(self,
                 x : int,
                 y : int,
                 torus : bool = False) :
        super(BoxModel, self).__init__()
        self.grid : MultiGrid = MultiGrid(x, y, torus)
        self.agent_list : List[PortrayedAgent] = []
        self.box_list   : List[Box] = []
        self.platform : Optional[Destination] = None
        self.platform_pos : Tuple[int, int] = (0, 0)

