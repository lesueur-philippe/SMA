from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from collectors import get_nb_carrying, get_remaining_boxes


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

    def move(self) :
        possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore = True, include_center = False
        )
        if (self.carrying) :
            new_position = min(possible_steps)
        else :
            new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def pickup_box(self, box : BoxAgent) :
        print(f"Box : w -> {box.weight}, id -> {box.unique_id}")
        self.carrying = True
        self.currently_carrying += box.weight
        # del self.model.boxes[box.unique_id]
        self.model.schedule.remove(box)
        self.model.grid.remove_agent(box)

    def drop_box(self) :
        print(f"Agent dropped box of weight {self.currently_carrying}")
        self.carrying = False
        self.currently_carrying = 0

    def step(self) :
        self.move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        boxes = [agent for agent in cellmates if isinstance(agent, BoxAgent)]
        #print(boxes)
        if len(boxes) > 0 :
            self.pickup_box(boxes[0])

        if self.pos == (0, 0) :
            self.drop_box()


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
            self.grid.place_agent(agent, (0, 0))

        for i in range(self.nb_boxes) :
            index = i + self.nb_agents
            box = BoxAgent(index, self, 5)

            self.schedule.add(box)
            self.boxes[index] = box

            x = self.random.randrange(1, self.grid.width)
            y = self.random.randrange(1, self.grid.height)

            self.grid.place_agent(box, (x, y))

        dest = DestinationAgent(nb_agents + nb_boxes, self)
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

