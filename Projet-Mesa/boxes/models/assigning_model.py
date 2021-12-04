import numpy as np

from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from ..agents import Box, Destination, SmartAgent
from .grid_model import GridModel
from ..utils.collectors import get_nb_carrying, get_remaining_boxes
from ..utils import get_distance


class AssigningModel(GridModel) :
    
    def __init__(self,
                 nb_agents : int,
                 nb_boxes : int,
                 width : int,
                 height : int,
                 torus : bool = False) :
        super(AssigningModel, self).__init__(width, height, torus)
        self.nb_agents = nb_agents
        self.nb_boxes = nb_boxes
        self.schedule = RandomActivation(self)
        self.running = True
        self.carriers = {}
        self.boxes = {}

        # Populate
        for i in range(self.nb_agents) :
            agent = SmartAgent(i, self, strength = 10)
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

        self.platform = Destination(nb_agents + nb_boxes, self)
        self.platform_pos = (0, 0)
        self.schedule.add(self.platform)
        self.grid.place_agent(self.platform, self.platform_pos)

        # Add data collection
        self.data_collectors = DataCollector(
                model_reporters = {"Carrying" : get_nb_carrying,
                                   "Boxes"    : get_remaining_boxes}
        )

    # task assignment
    # agents_targets_matrix is the matrix of effort for a box/agent pair
    # agents_index is the index of the agents that search for a box
    # agents_index is the index of the boxes to be allocated
    def box_allocation(self, agents_targets_matrix, agents_index, boxes_index) :

        atm = agents_targets_matrix.copy()
        ags = np.sum(atm, axis = 1)  # agents global score
        agents = agents_index.copy()
        boxes = boxes_index.copy()
        if len(atm) == 0 :
            return self
        # checking if there are more tasks than workers
        if len(atm) < len(atm[0]) :
            # while all workers don't have a box assigned
            while len(agents) != 0 :
                ind_agent = np.argmax(ags)
                ind_box = np.argmin(atm[ind_agent])
                self.carriers[agents[ind_agent]].assign_box(self.boxes[boxes[ind_box]])
                atm = np.delete(atm, ind_box, axis = 1)
                atm = np.delete(atm, ind_agent, axis = 0)
                ags = np.delete(ags, ind_agent)
                agents = np.delete(agents, ind_agent)
                boxes = np.delete(boxes, ind_box)
        else :
            # while all box aren't assigned to an agent
            while len(boxes) != 0 :
                ind_agent = np.argmin(ags)
                ind_box = np.argmin(atm[ind_agent])
                self.carriers[agents[ind_agent]].assign_box(self.boxes[boxes[ind_box]])
                atm = np.delete(atm, ind_box, axis = 1)
                atm = np.delete(atm, ind_agent, axis = 0)
                ags = np.delete(ags, ind_agent)
                agents = np.delete(agents, ind_agent)
                boxes = np.delete(boxes, ind_box)
        return self

    def target_attribution(self) :
        agent_ind = []
        attributed = []
        box_ind = []

        for carrier in self.carriers :
            agent = self.carriers[carrier]
            if agent.target_box is None :
                agent_ind.append(carrier)
            if agent.carried_box is not None :
                attributed.append(agent.target_box)

        for b in self.boxes:
            if not self.boxes[b] in attributed :
                box_ind.append(b)

        distance_matrix = np.zeros((len(agent_ind), len(box_ind)))

        for i in range(len(agent_ind)) :
            for j in range(len(box_ind)) :
                distance_matrix[i, j] = get_distance(self.carriers[agent_ind[i]].pos, self.boxes[box_ind[j]].pos)
        self.box_allocation(distance_matrix, agent_ind, box_ind)

    def step(self) -> None :
        self.data_collectors.collect(self)
        self.target_attribution()
        self.schedule.step()
