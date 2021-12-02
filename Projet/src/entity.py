import numpy as np


class Entity:
    grid = None
    cell = None
    weight = None

    def __init__(self, grid, weight=1):
        self.grid = grid
        self.weight = weight

    def get_position(self):
        return self.cell.get_coordinates()

    def get_weight(self):
        return self.weight

    def is_passive(self):
        return True

    def is_active(self):
        return not self.is_passive()

    def is_agent(self):
        return False

    def is_box(self):
        return False

    def is_platform(self):
        return False

    def add_weight(self, n):
        self.weight += n

    def get_grid(self):
        return self.grid

    def get_cell(self):
        return self.cell

    def set_cell(self, cell):
        self.cell = cell
        return self

    def distance_to(self, entity):
        x, y = self.get_position()
        x2, y2 = entity.get_position()
        return np.abs(x - x2) + np.abs(y - y2)

    def is_adjacent(self, entity):
        return self.distance_to(entity) == 1


class ActiveEntity(Entity):
    box = None
    strategy = None
    labour = 0

    def has_box(self):
        return self.box is not None

    def set_box(self, box):
        self.box = box
        return self

    def take_box(self, box):
        assert (not self.has_box)
        assert (self.can_hold_box(box))
        self.labour += 1
        self.box = box
        return self

    def can_hold_box(self, box):
        return self.get_weight() >= box.get_weight()

    def is_passive(self):
        return False

    def wait(self):
        pass

    def move_up(self):
        self.labour += 1
        cell = self.get_cell()
        x, y = self.get_position()
        assert x - 1 >= 0, "Inutile de vouloir vous échapper."
        self.get_grid().place_entity(x - 1, y, self)
        cell.set_entity(None)
        return self

    def move_down(self):
        self.labour += 1
        cell = self.get_cell()
        x, y = self.get_position()
        assert x + 1 < self.get_grid().get_height(), "Inutile de vouloir vous échapper."
        self.get_grid().place_entity(x + 1, y, self)
        cell.set_entity(None)
        return self

    def move_left(self):
        self.labour += 1
        cell = self.get_cell()
        x, y = self.get_position()
        assert y - 1 >= 0, "Inutile de vouloir vous échapper."
        self.get_grid().place_entity(x, y - 1, self)
        cell.set_entity(None)
        return self

    def move_right(self):
        self.labour += 1
        cell = self.get_cell()
        x, y = self.get_position()
        assert y + 1 < self.get_grid().get_width(), "Inutile de vouloir vous échapper."
        self.get_grid().place_entity(x, y + 1, self)
        cell.set_entity(None)
        return self

    def transfer_box(self, entity):
        self.labour += 1
        assert entity.get_cell() is None
        entity.set_box(self.get_box())
        self.set_box(None)
        return self

    def aggregate(self, group):
        assert not self.has_box()
        assert not group.has_box()
        self.labour += 1
        if self.is_group():
            if group.is_group():
                for a in group.get_agents():
                    self.add_agent(a)
                group.get_cell().pop_entity()
            else:
                self.add_agent(group)
                group.get_cell().pop_entity()
        else:
            if group.is_group():
                group.add_agent(self)
                group.get_cell().pop_entity()
                group.set_cell(self.get_cell())
            else:
                new_group = AgentsTeam(self.grid)
                new_group.add_agent(self)
                new_group.add_agent(group)
                cell = self.get_cell()
                cell.pop_entity()
                cell.set_entity(new_group)
                new_group.set_cell(cell)
        return self

    def deposit_box(self, platform):
        assert platform.is_platform()
        self.get_grid().remove(self.box)
        self.box = None


class Agent(ActiveEntity):

    def __init__(self, grid, weight=1):
        super().__init__(grid, weight=weight)

    def leave_group_up(self, group):
        x, y = group.get_position()
        self.set_cell(x-1, y)
        self.get_grid().get_cell(x-1, y).set_entity(self)
        group.remove_agent(self)
        return self

    def is_agent(self):
        return True

    def is_group(self):
        return False


class AgentsTeam(Agent):

    agents = []

    def __init__(self, grid, weight=0):
        super().__init__(grid, weight=weight)

    def add_agent(self, agent):
        self.agents.append(agent)
        self.add_weight(1)
        return self

    def remove_agent(self, agent):
        self.agents.remove(agent)
        self.add_weight(-1)
        return self

    def is_group(self):
        return True


class Platform(Entity):
    boxes = []

    def __init__(self, grid, weight=999):
        super().__init__(grid, weight=weight)

    def is_platform(self):
        return True


class Box(Entity):

    def is_box(self):
        return True
