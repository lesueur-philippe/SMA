import sys
sys.path.insert(1, '../src')
import unittest
import grid
import entity

class Entity_test(unittest.TestCase):

    def test_get_position(self):
        g = grid.Grid(10,5,[],0)
        x = 3
        y = 3
        ent = entity.Entity(g)
        g.place_entity(x, y, ent)
        return ent.get_position() == (x,y)

    def test_add_weight(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        ent.add_weight(3)
        return ent.get_weight() == 4

    def test_get_weight(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        nent = entity.Entity(g, weight=8)
        return (ent.get_weight(), nent.get_weight()) == (1,8)

    def test_is_passive(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        return ent.is_passive()

    def test_is_active(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        return ent.is_active()

    def test_is_agent(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        return not ent.is_agent()

    def test_is_box(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        return not ent.is_box()

    def test_is_plateform(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        return not ent.is_platform()

    def test_is_active(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        return not ent.is_active()

    def test_get_cell(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        cell = grid.Grid_cells(0, 0)
        ent.set_cell(cell)
        return ent.get_cell() == cell

    def test_distance_to(self):
        g = grid.Grid(10,5,[],0)
        x = 3
        y = 3
        ent = entity.Entity(g)
        g.place_entity(x, y, ent)
        nent = entity.Entity(g)
        g.place_entity(x+2, y-1, nent)
        return ent.distance_to(nent) == 3

    def test_is_adjacente_true(self):
        g = grid.Grid(10,5,[],0)
        x = 3
        y = 3
        ent = entity.Entity(g)
        g.place_entity(x, y, ent)
        nent = entity.Entity(g)
        g.place_entity(x, y-1, nent)
        return ent.is_adjacent(nent)

    def test_is_adjacente_false(self):
        g = grid.Grid(10,5,[],0)
        x = 3
        y = 3
        ent = entity.Entity(g)
        g.place_entity(x, y, ent)
        nent = entity.Entity(g)
        g.place_entity(x+1, y-1, nent)
        return not ent.is_adjacent(nent)

class ActiveEntity_test(unittest.TestCase):

    def test_is_active(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.ActiveEntity(g)
        return ent.is_active()


