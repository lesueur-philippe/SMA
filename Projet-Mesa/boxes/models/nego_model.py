from typing import Callable

import numpy as np

from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from ..agents import Box, Destination, NegotiatingAgent
from .box_model import BoxModel
from ..utils.collectors import get_nb_carrying, get_remaining_boxes
from ..utils import get_distance
from copy import deepcopy


class NegoModel(BoxModel) :

    def __init__(self,
                 nb_agents : int,
                 nb_boxes : int,
                 width : int,
                 height : int,
                 torus : bool = False) :
        super(NegoModel, self).__init__(width, height, torus)
        self.nb_agents = nb_agents
        self.nb_boxes  = nb_boxes
        self.schedule  = RandomActivation(self)
        self.running   = True
        self.carriers  = {}
        self.boxes     = {}

        # Populate
        for i in range(self.nb_agents) :
            agent = NegotiatingAgent(i, self, strength = 10)
            self.schedule.add(agent)
            self.carriers[i] = agent
            self.agent_list.append(agent)
            self.grid.place_agent(agent, ((i + 1) % self.grid.width, (i + 1) // self.grid.width))

        for i in range(self.nb_boxes) :
            index = i + self.nb_agents
            box = Box(index, self)

            # self.schedule.add(box)
            self.boxes[index] = box
            self.box_list.append(box)

            x = self.random.randrange(1, self.grid.width)
            y = self.random.randrange(1, self.grid.height)

            self.grid.place_agent(box, (x, y))

        self.platform     = Destination(nb_agents + nb_boxes, self)
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
            # while all agents don't have a box assigned
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
            # while all boxes aren't assigned to an agent
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
            if isinstance(agent.target_box, Box) :
                attributed.append(agent.target_box)

        for b in self.boxes :
            if not self.boxes[b] in attributed :
                box_ind.append(b)

        distance_matrix = np.zeros((len(agent_ind), len(box_ind)))
        for i in range(len(agent_ind)) :
            for j in range(len(box_ind)) :
                distance_matrix[i, j] = get_distance(self.carriers[agent_ind[i]].pos, self.boxes[box_ind[j]].pos)
        self.box_allocation(distance_matrix, agent_ind, box_ind)

    def solve_conflict(self, agent1, agent2) :
        # check agent2 already negociated this step
        if not agent2.negociated and agent2.round == agent1.round :
            agent2.available_next_steps()
        a1_pos = agent1.wished_positions.copy()
        a2_pos = agent2.wished_positions.copy()
        a1p = deepcopy(agent1.pos)
        a2p = deepcopy(agent2.pos)
        for pos in a1_pos :
            if pos in a2_pos :
                # if there are enough positions available, delete one
                if len(agent1.wished_positions) > len(agent2.wished_positions) :
                    agent1.wished_positions.remove(pos)
                # if there are enough positions available, delete one
                elif len(agent2.wished_positions) > len(agent1.wished_positions) :
                    agent2.wished_positions.remove(pos)
                # if there are equal number of available positions
                elif len(agent1.wished_positions) == 1 and len(agent2.wished_positions) == 1 :
                    if agent1.target_box is None :
                        if agent2.target_box is None :
                            agent2.wished_positions = [a2p]
                        else :
                            print(agent2.target_box)
                            print(agent2.target_box.pos)
                            if get_distance(agent2.target_pos, a1p) < get_distance(agent2.target_pos, a2p) :
                                if get_distance(a1p, a2p) == 1 :
                                    agent1.wished_positions = [a2p]
                                    agent2.wished_positions = [a1p]
                                else :
                                    agent1.wished_positions = [a1p]
                    elif agent2.target_box is None :
                        if agent1.target_box is None :
                            agent1.wished_positions = [a1p]
                        else :
                            if get_distance(agent1.target_pos, a2p) < get_distance(agent1.target_pos, a1p) :
                                if get_distance(a2p, a1p) == 1 :
                                    agent1.wished_positions = [a2p]
                                    agent2.wished_positions = [a1p]
                                else :
                                    agent2.wished_positions = [a2p]

        agent1.negociated = True
        agent1.negociated_with.append(agent2)
        agent2.negociated = True
        agent2.negociated_with.append(agent1)

    def step(self) -> None :
        self.data_collectors.collect(self)
        self.target_attribution()

        for agent in self.agent_list :
            agent.compute_possible_steps()

        self.schedule.step()
