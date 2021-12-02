class AgentStrategy:
    
    entity=None
    
    def __init__(self, entity):
        self.entity = entity

    """
    Returns the chained list of the entities to go towards (or act upon) sorted by effort.
    """
    def find(self):
        pass

    """
    Adding to/Creating a sorted list of the different boxes.
    Boxes are sorted by effort which correspond to their distance (regardless of box's weight)
    """
    def sorted_insert(box, distance, current):
        if (current is None) or (current["distance"] > distance):
            return {"target":box, "distance":distance, "next": current}
        new_current = current
        while not (new_current["next"] is None) and new_current["next"]["distance"] < distance:
            new_current = new_current["next"]
        chain = {"target":box, "distance":distance, "next": new_current["next"]}
        new_current["next"] = chain
        return current

    def do(self):
        pass
    
    """
    Boolean function for verifying current strategy
    ==> Verify if instance is BoxGatheringStrategy
    """
    def is_Gathering(self):
        return False
    
    """
    Boolean function for verifying current strategy
    ==> Verify if instance is BoxDepositingStrategy
    """
    def is_Depositing(self):
        return False


class BoxGatheringStrategy(AgentStrategy):

    """
    Returns the chained list of the entities to go towards (or act upon) sorted by effort.
    """
    def find(self):
        chain = None
        for box in self.entity.get_grid().get_boxes():
            chain = self.sorted_insert(box, self.entity.distance_to(box), chain)
        """
        agent_chain = None
        for agent in self.entity.get_grid().get_agents():
            agent_chain = self.sorted_insert_agent(agent, self.entity.distance_to(agent),  agent_chain)
        """
        return chain
    
    """
    Boolean function for verifying current strategy
    ==> Verify if instance is BoxGatheringStrategy
    """
    def is_Gathering(self):
        return True
            

class BoxDepositingStrategy(AgentStrategy):

    """
    Returns the chained list of the entities to go towards (or act upon) sorted by effort.
    """
    def find(self):
        return self.sorted_insert(entity.get_grid().get_plateform(), self.entity.distance_to(entity.get_grid().get_plateform()), None)
    
    """
    Boolean function for verifying current strategy
    ==> Verify if instance is BoxDepositingStrategy
    """
    def is_Depositing(self):
        return True