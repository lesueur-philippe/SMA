from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from collectors import get_nb_carrying, get_remaining_boxes
import numpy as np


class GridModel(Model) :
    def __init__(self,
                 width : int,
                 height : int,
                 torus : bool) :
        super(GridModel, self).__init__()
        self.grid = MultiGrid(width, height, torus)


class BoxAgent(Agent) :
    def __init__(self,
                 unique_id : int,
                 model : GridModel,
                 weight : int) :
        super(BoxAgent, self).__init__(unique_id, model)
        self.weight = weight


class CarrierAgent(Agent) :

    def __init__(self,
                 unique_id : int,
                 model : GridModel,
                 strength : int) :
        super(CarrierAgent, self).__init__(unique_id, model)
        self.carrying = False
        self.target_box = None
        self.strength = strength
        self.currently_carrying = 0
        self.next_steps = None
        self.holded_box = None

    def move(self, new_position) :
        self.model.grid.move_agent(self, new_position)
    
    def next_possible_steps(self) :
        possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore = False, include_center = True
        )
        try:
            target_position = self.target_box.pos
        except AttributeError:
            self.next_steps = [possible_steps[0]]
            return self
        distances = [self.model.get_distance_from(target_position, step) for step in possible_steps]
        distance = self.model.get_distance_from(target_position, self.pos)
        next_steps = []
        for i in range(len(distances)):
            if distances[i] < distance:
                next_steps.append(possible_steps[i])
        if len(next_steps) == 0:
            next_steps.append(self.pos)
        self.next_steps = next_steps

    def pickup_box(self, box : BoxAgent) :
        print(f"Box : w -> {box.weight}, id -> {box.unique_id}")
        self.carrying = True
        self.currently_carrying = box.weight
        self.target_box = self.model.platform
        self.holded_box = box
        del self.model.boxes[self.holded_box.unique_id]
        self.model.schedule.remove(box)
        self.model.grid.remove_agent(box)

    def drop_box(self) :
        print(f"Agent dropped box of weight {self.currently_carrying}")
        self.carrying = False
        self.currently_carrying = 0
        self.target_box = None
        self.holded_box = None
        self.model.target_attribution()

    def step(self) :
        cellmates = self.model.grid.get_cell_list_contents(self.model.grid.get_neighborhood(
                self.pos, moore = False, include_center = False
        ))
        boxes = [agent for agent in cellmates if (isinstance(agent, BoxAgent) or isinstance(agent, DestinationAgent))]
        for b in boxes:
            if (not self.carrying) and b == self.target_box:
                self.pickup_box(b)
                return self
            elif self.carrying and isinstance(b, DestinationAgent):
                self.drop_box()
                self.target_box = None
                return self
        self.next_possible_steps()
        self.move(self.next_steps[0])


class DestinationAgent(Agent) :
    def __init__(self, 
                 unique_id : int, 
                 model : GridModel) :
        super(DestinationAgent, self).__init__(unique_id, model)



class BoxModel(GridModel) :
    def __init__(self,
                 nb_agents : int,
                 nb_boxes : int,
                 width : int,
                 height : int,
                 torus : bool) :
        super(BoxModel, self).__init__(width, height, torus)
        self.nb_agents = nb_agents
        self.nb_boxes = nb_boxes
        self.schedule = RandomActivation(self)
        self.running = True
        self.carriers = {}
        self.boxes = {}
        
        # Populate
        for i in range(self.nb_agents) :
            agent = CarrierAgent(i, self, 10)
            self.schedule.add(agent)
            self.carriers[i] = agent
            
            x = i+1%self.grid.width
            y = (i+1)//self.grid.width
            self.grid.place_agent(agent, (x, y))

        for i in range(0, self.nb_boxes) :
            index = i + self.nb_agents
            box = BoxAgent(index, self, 1)

            self.schedule.add(box)
            self.boxes[index] = box

            x = self.random.randrange(1, self.grid.width)
            y = self.random.randrange(1, self.grid.height)

            self.grid.place_agent(box, (x, y))

        dest = DestinationAgent(nb_agents + nb_boxes, self)
        self.schedule.add(dest)
        self.grid.place_agent(dest, (0, 0))
        self.platform = dest

        # Add data collection
        self.data_collectors = DataCollector(
                model_reporters = {"Carrying" : get_nb_carrying,
                                   "Boxes" : get_remaining_boxes}
        )


    # task assignement
    # agents_targets_matrix is the matrix of effort for a pair box/agent
    # agents_index is the index of the agents that search for a box
    # agents_index is the index of the boxes to be allocated
    def box_allocation(self, agents_targets_matrix, agents_index, boxes_index):
        atm = agents_targets_matrix.copy()
        ags = np.sum(atm, axis=1)  # agents global score
        agents = agents_index.copy()
        boxes = boxes_index.copy()
        if len(atm) == 0:
            return self
        # checking if there are more tasks than workers
        if len(atm) < len(atm[0]):
            # while all worker don't have a box assigned
            while len(agents) != 0:
                ind_agent = np.argmax(ags)
                ind_box = np.argmin(atm[ind_agent])
                self.carriers[agents[ind_agent]].target_box = self.boxes[boxes[ind_box]]
                atm = np.delete(atm, ind_box, axis=1)
                atm = np.delete(atm, ind_agent, axis=0)
                ags = np.delete(ags, ind_agent)
                agents = np.delete(agents, ind_agent)
                boxes = np.delete(boxes, ind_box)
        else:
            # while all box aren't assigned to an agent
            while len(boxes) != 0:
                ind_agent = np.argmin(ags)
                ind_box = np.argmin(atm[ind_agent])
                self.carriers[agents[ind_agent]].target_box = self.boxes[boxes[ind_box]]
                atm = np.delete(atm, ind_box, axis=1)
                atm = np.delete(atm, ind_agent, axis=0)
                ags = np.delete(ags, ind_agent)
                agents = np.delete(agents, ind_agent)
                boxes = np.delete(boxes, ind_box)
        return self

    def get_distance_from(self, pos1, pos2):
        return np.abs(pos1[0] - pos2[0]) + np.abs(pos1[1] - pos2[1])

    def target_attribution(self):
        agent_ind = []
        attributed = []
        for a in self.carriers:
            if self.carriers[a].target_box is None:
                agent_ind.append(a)
            if isinstance(self.carriers[a].target_box, BoxAgent):
                attributed.append(self.carriers[a].target_box)
            if not self.carriers[a].holded_box is None:
                attributed.append(self.carriers[a].target_box)
        box_ind = []
        for b in self.boxes:
            if not self.boxes[b] in attributed:
                box_ind.append(b)
        distance_matrix = np.zeros((len(agent_ind), len(box_ind)))
        for i in range(len(agent_ind)):
            for j in range(len(box_ind)):
                distance_matrix[i,j] = self.get_distance_from(self.carriers[agent_ind[i]].pos, self.boxes[box_ind[j]].pos)
        self.box_allocation(distance_matrix, agent_ind, box_ind)

    def step(self) -> None :
        self.data_collectors.collect(self)
        self.target_attribution()
        self.schedule.step()

