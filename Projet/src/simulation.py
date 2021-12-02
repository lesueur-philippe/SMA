import numpy as np
import strategy
import grid


class Simulation:
    grid = None
    nbTours = 0
    available_boxes = None

    def __init__(self, height, width, nbBoxes, nbAgents, boxSizeMax):
        boxes = np.random.randint(1, high=boxSizeMax + 1, size=nbBoxes)
        self.grid = grid.Grid(height, width, boxes, nbAgents)
        self.available_boxes = self.grid.get_boxes().copy()

    def play(self):
        agents = self.grid.get_agents()
        for a in agents:
            a.set_strategy(strategy.BoxGatheringStrategy(a))
        while not len(self.grid.get_boxes()) == 0:
            self.next_step()
            self.nbTours += 1
        return self.nbTours
    
    """
    Says if the entity can move to coordinates.
    """
    def can_move(self, x, y):
        if (x < 0) | (x >= self.grid.height) | (y < 0) | (x >= self.grid.width):
            return False
        elif not self.grid.get_cell(x, y).is_empty():
            return False
        else:
            return True
    """
    stay on same cell : 0
    go one cell upwards : 1
    go one cell downwards : 2
    go one cell to the left : 3
    go one cell to the right : 4
    grab a box on the upwards cell: 5
    grab a box on the downwards cell: 6
    grab a box on the left cell: 7
    grab a box on the right cell: 8
    transfer box to the upwards agent: 9
    transfer box to the downwards agent: 10
    transfer a box to the agent to the left: 11
    transfer a box to the agent to the right: 12
    drop box on the upwards cell: 13
    drop box on the downwards cell: 14
    drop box on the left cell: 15
    drop box on the right cell: 16
    """
    def step(self, entity, action):
        x, y = entity.get_position()
        if action == 0:
            entity.wait()
            return entity.get_position(), self.reward(action)
        if action == 1:
            if self.can_move(x-1, y):
                entity.move_up()
                return entity.get_position(), self.reward(action)
            else:
                new_action = self.solve_move(x-1, y, entity)
                return self.step(entity, new_action)
        if action == 2:
            if self.can_move(x+1, y):
                entity.move_down()
                return entity.get_position(), self.reward(action)
            else:
                new_action = self.solve_move(x+1, y, entity)
                return self.step(entity, new_action)
        if action == 3:
            if self.can_move(x, y-1):
                entity.move_left()
                return entity.get_position(), self.reward(action)
            else:
                new_action = self.solve_move(x, y-1, entity)
                return self.step(entity, new_action)
        if action == 4:
            if self.can_move(x, y+1):
                entity.move_right()
                return entity.get_position(), self.reward(action)
            else:
                new_action = self.solve_move(x, y+1, entity)
                return self.step(entity, new_action)
        if action == 5:
            if entity.has_box():
                entity.set_strategy(strategy.BoxDepositingStrategy(entity))
            else:
                if not self.grid.get_cell(x-1, y).is_empty():
                    if self.grid.get_cell(x-1, y).get_entity().is_box():
                        entity.take_box(self.grid.get_cell(x-1, y).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 6:
            if entity.has_box():
                entity.set_strategy(strategy.BoxDepositingStrategy(entity))
            else:
                if not self.grid.get_cell(x+1, y).is_empty():
                    if self.grid.get_cell(x+1, y).get_entity().is_box():
                        entity.take_box(self.grid.get_cell(x+1, y).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 7:
            if entity.has_box():
                entity.set_strategy(strategy.BoxDepositingStrategy(entity))
            else:
                if not self.grid.get_cell(x, y-1).is_empty():
                    if self.grid.get_cell(x, y-1).get_entity().is_box():
                        entity.take_box(self.grid.get_cell(x, y-1).get_entity())
                    return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 8:
            if entity.has_box():
                entity.set_strategy(strategy.BoxDepositingStrategy(entity))
            else:
                if not self.grid.get_cell(x, y+1).is_empty():
                    if self.grid.get_cell(x, y+1).get_entity().is_box():
                        entity.take_box(self.grid.get_cell(x, y+1).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 9:
            if entity.has_box():
                if not self.grid.get_cell(x-1, y).is_empty():
                    if self.grid.get_cell(x-1, y).get_entity().is_agent():
                        entity.transfer_box(self.grid.get_cell(x-1, y).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 10:
            if entity.has_box():
                if not self.grid.get_cell(x+1, y).is_empty():
                    if self.grid.get_cell(x+1, y).get_entity().is_agent():
                        entity.transfer_box(self.grid.get_cell(x+1, y).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 11:
            if entity.has_box():
                if not self.grid.get_cell(x, y-1).is_empty():
                    if self.grid.get_cell(x, y-1).get_entity().is_agent():
                        entity.transfer_box(self.grid.get_cell(x, y-1).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 12:
            if entity.has_box():
                if not self.grid.get_cell(x, y+1).is_empty():
                    if self.grid.get_cell(x, y+1).get_entity().is_agent():
                        entity.transfer_box(self.grid.get_cell(x, y+1).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 13:
            if entity.has_box():
                if not self.grid.get_cell(x-1, y).is_empty():
                    if self.grid.get_cell(x-1, y).get_entity().is_agent():
                        entity.deposit_box(self.grid.get_cell(x-1, y).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 14:
            if entity.has_box():
                if not self.grid.get_cell(x+1, y).is_empty():
                    if self.grid.get_cell(x+1, y).get_entity().is_agent():
                        entity.deposit_box(self.grid.get_cell(x+1, y).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 15:
            if entity.has_box():
                if not self.grid.get_cell(x, y-1).is_empty():
                    if self.grid.get_cell(x, y-1).get_entity().is_agent():
                        entity.deposit_box(self.grid.get_cell(x, y-1).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)
        if action == 16:
            if entity.has_box():
                if not self.grid.get_cell(x, y+1).is_empty():
                    if self.grid.get_cell(x, y+1).get_entity().is_agent():
                        entity.deposit_box(self.grid.get_cell(x, y+1).get_entity())
                        return entity.get_position(), self.reward(action)
            return entity.get_position(), self.reward(0)

    # definition of rewards in case a deep learning approach of the multi-agent problem
    # we did not have the time to implement the deep learning algorithm
    @staticmethod
    def reward(action):
        if (action > 4) and (action < 9):
            return 5
        if (action > 12) and (action < 17):
            return 10
        else:
            return 0
    """
    Choosing and executing an action for each agent.
    First each agent chooses a wished target
    Then get_action gives the action to be executed according to negotiated targets
    """
    def next_step(self):
        agent_find = {}
        for agent in self.grid.get_agents():
            agent_find[agent] = agent.get_strategy().find()
        agent_actions = self.get_actions(agent_find)
        for ag, ac in agent_actions:
            self.step(self, ac, ag)
        return self
    
    
    def get_actions(self, agents_targets):
        first_target = self.target_allocation(agents_targets)
        final_target = self.negociate(first_target)
        actions = self.target_to_action(final_target)
        return actions
                    
    def target_allocation(self, agents_targets):
        a_t = {}
        min = {}

        for box in self.grid.get_boxes():
            min[box] = []
        for agent in agents_targets:
            min[agents_targets[agent]["target"]].append((agent, agents_targets[agent]["distance"]))
        res = []
        # while there are conflicts
        while len(res) != len(agents_targets):
            unallocated = []
            for box in self.grid.get_boxes():
                box_neociation = min[box]
                





                
                
        
