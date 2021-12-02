import numpy as np
import entity


class Grid:
    grid = None
    boxes = []
    agents = []
    platform = None
    height = None
    width = None

    def __init__(self, height=10, width=10, boxes=None, agents_number=4):
        if boxes is None:
            boxes = []
        assert len(boxes) + agents_number < (
                    height * width) / 2, 'Veuillez augmenter la taille de la grille ou réduire le nombre d\'entités'
        for box in boxes:
            assert box <= agents_number, 'Il n\'y a pas suffisement d\'agents pour pouvoir porter toutes les boîtes.'
        self.height = height
        self.width = width
        self.grid = np.empty((0, width))
        for i in range(height):
            line = []
            for j in range(width):
                cell = Grid_cells(i, j)
                line.append(cell)
            self.grid = np.append(self.grid, np.array([line]), axis=0)
        self.set_agents(agents_number)
        self.set_platform()
        self.set_boxes(boxes)

    def get_cell(self, x, y):
        return self.grid[x, y]

    def get_agents(self):
        return self.agents

    def get_boxes(self):
        return self.boxes

    def remove_box(self, box):
        self.boxes.remove(box)
        return self

    def set_platform(self):
        platform = entity.Platform(self.grid)
        self.random_place(platform)
        self.platform = platform
        return self

    def set_agents(self, agents_number):
        for i in range(agents_number):
            agent = entity.Agent(self.grid)
            self.random_place(agent)
            self.agents.append(agent)
        return self

    def set_boxes(self, boxes):
        for box in boxes:
            nbox = entity.Box(self, weight=box)
            self.random_place(nbox)
            self.boxes.append(nbox)
        return self

    def random_place(self, e):
        x = np.random.randint(self.height)
        y = np.random.randint(self.width)
        while not self.grid[x, y].is_empty():
            x = np.random.randint(self.height)
            y = np.random.randint(self.width)
        self.place_entity(x, y, e)
        return self

    def place_entity(self, x, y, e):
        self.grid[x, y].set_entity(e)
        e.set_cell(self.grid[x, y])
        return self


class Grid_cells:
    x = None
    y = None
    entity = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_empty(self):
        return self.entity is None

    def get_coordinates(self):
        return self.x, self.y

    def set_entity(self, e):
        assert self.is_empty()
        self.entity = e
        return self

    def get_entity(self):
        return self.entity

    def pop_entity(self):
        e = self.entity
        self.entity = None
        return e
