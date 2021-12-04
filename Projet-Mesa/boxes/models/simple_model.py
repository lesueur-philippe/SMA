from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from ..utils.collectors import get_nb_carrying, get_remaining_boxes

from ..agents.dummy_agent import DummyAgent
from ..agents.props import Box, Destination
from .grid_model import GridModel


class SimpleModel(GridModel) :
    def __init__(self,
                 nb_agents : int,
                 nb_boxes : int,
                 width : int,
                 height : int,
                 torus : bool) :
        super(SimpleModel, self).__init__(width, height, torus)
        self.nb_agents = nb_agents
        self.nb_boxes = nb_boxes
        self.schedule = RandomActivation(self)
        self.running = True
        self.carriers = {}
        self.boxes = {}

        # Populate
        for i in range(self.nb_agents) :
            agent = DummyAgent(i, self, strength = 10)
            self.schedule.add(agent)
            self.carriers[i] = agent
            self.grid.place_agent(agent, (0, 0))

        for i in range(self.nb_boxes) :
            index = i + self.nb_agents
            box = Box(index, self)

            self.schedule.add(box)
            self.boxes[index] = box

            x = self.random.randrange(1, self.grid.width)
            y = self.random.randrange(1, self.grid.height)

            self.grid.place_agent(box, (x, y))

        dest = Destination(nb_agents + nb_boxes, self)
        self.schedule.add(dest)
        self.grid.place_agent(dest, (0, 0))

        # Add data collection
        self.data_collectors = DataCollector(
                model_reporters = {"Carrying" : get_nb_carrying,
                                   "Boxes" : get_remaining_boxes}
        )

    def step(self) -> None :
        self.data_collectors.collect(self)
        self.schedule.step()

