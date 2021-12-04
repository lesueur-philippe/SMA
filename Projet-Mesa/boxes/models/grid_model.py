from mesa import Model
from mesa.space import MultiGrid


class GridModel(Model) :
    def __init__(self,
                 width  : int,
                 height : int,
                 torus  : bool = False) :
        super(GridModel, self).__init__()
        self.grid = MultiGrid(width, height, torus)
