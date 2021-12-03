from typing import Dict, Union

from mesa import Agent, Model

from ..portrayed_agent import PortrayedAgent


class Destination(PortrayedAgent) :
    """
    A class to represent the destination cell on the grid.
    """

    def __init__(self,
                 unique_id : int,
                 model : Model) :
        """
        Generates the cell

        :param unique_id: the id for the cell
        :param model: the model the cell is related to
        """
        
        super(Destination, self).__init__(unique_id, model)

    def portray(self) -> Dict[str, Union[str, float]] :
        return {
            "Shape"  : "circle",
            "Filled" : "true",
            "r"      : 0.8,
            "Layer"  : 0,
            "Color"  : "#EF767A"
        }

    def step(self) -> None :
        pass
