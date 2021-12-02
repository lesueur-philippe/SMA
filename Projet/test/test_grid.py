import sys
sys.path.insert(1, '../src')
import unittest
import grid
import entity

class Grid_test(unittest.TestCase):
    
    def test_init_height(self):
        g = grid.Grid(10,5,[],0)
        try :
            g.get_cell(9,0)
        except IndexError:
            return False
        try :
            g.get_cell(10,0)
        except IndexError:
            return True
        return False
    
    def test_init_width(self):
        g = grid.Grid(10,5,[],0)
        try :
            g.get_cell(0,4)
        except IndexError:
            return False
        try :
            g.get_cell(0,5)
        except IndexError:
            return True
        return False
    
    def test_init_places(self):
        try :
            grid.Grid(3,2,[],2)
            grid.Grid(3,2,[1],1)
        except IndexError:
            return False
        try :
            grid.Grid(3,2,[],3)
        except AssertionError:
            return True
        return False
            
    
    def test_init_boxes(self):
        g = grid.Grid(5,5,[1, 2, 4, 5],5)
        return len(g.get_boxes()) == 4
    
    def test_init_box_weight(self):
        try:
            grid.Grid(5,5,[2],1)
        except AssertionError:
            return True
        return False
    
    def test_init_agents(self):
        g = grid.Grid(5,5,[],3)
        return len(g.get_agents()) == 3
        
    def test_get_cell(self):
        g = grid.Grid(10,5,[],0)
        for x in range(10):
            for y in range(5):
                if g.get_cell(x,y).get_coordinates() != (x,y):
                    return False
        return True
        
    def test_set_plateform(self):
        g = grid.Grid(10,5,[],0)
        plat = False
        for x in range(10):
            for y in range(5):
                if g.get_cell(x,y).get_entity() != None:
                    if g.get_cell(x, y).get_entity().is_platform():
                        if not plat:
                            plat = not plat
                        else:
                            return False
        return plat
    
    def test_set_agent(self):
        g = grid.Grid(10,5,[],6)
        agents = 6
        for x in range(10):
            for y in range(5):
                if g.get_cell(x,y).get_entity() != None:
                    if g.get_cell(x,y).get_entity().is_agent():
                        if agents > 0:
                            agents -= 1
                        else:
                            return False
        return agents == 0
        
        
    def test_set_boxes(self):
        g = grid.Grid(10,5,[],6)
        boxes = [entity.Box(g), entity.Box(g), entity.Box(g), entity.Box(g)]
        for x in range(10):
            for y in range(5):
                if g.get_cell(x,y).get_entity() != None:
                    if g.get_cell(x,y).get_entity().is_box():
                        if len(boxes) > 0:
                            boxes.pop(g.get_cell(x,y).get_entity())
                        else:
                            return False
        return len(boxes) == 0
    
    def test_place_entity_grid(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        g.place_entity(3,3,ent)
        return g.get_cell(3,3).get_entity() == ent
        
    def test_place_entity_entity(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        g.place_entity(3,3,ent)
        return ent.get_cell() == g.get_cell(3,3)
    
    
class Grid_cells_test(unittest.TestCase):
    
    def test_is_empty_true(self):
        cell = grid.Grid_cells(0,0)
        return cell.is_empty()
    
    def test_is_empty_false(self):
        g = grid.Grid(10,5,[],0)
        cell = grid.Grid_cells(0,0)
        cell.set_entity(entity.Entity(g))
        return not cell.is_empty()
    
    def test_set_entity_entity(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        cell = grid.Grid_cells(0,0)
        cell.set_entity(ent)
        return cell.get_entity() == ent
        
    def test_set_entity_error(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        nent = entity.Entity(g)
        cell = grid.Grid_cells(0,0)
        cell.set_entity(ent)
        try :
            cell.set_entity(nent)
        except AssertionError:
            return True
        return False
        
    def test_pop_entity_entity(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        cell = grid.Grid_cells(0,0)
        cell.set_entity(ent)
        return cell.pop_entity() == ent
    
    def test_pop_entity_entity(self):
        g = grid.Grid(10,5,[],0)
        ent = entity.Entity(g)
        cell = grid.Grid_cells(0,0)
        cell.set_entity(ent)
        cell.pop_entity()
        return cell.is_empty()
