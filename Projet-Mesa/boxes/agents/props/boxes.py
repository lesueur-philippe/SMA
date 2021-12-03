from typing import Dict, Union

from mesa import Model

from ..portrayed_agent import PortrayedAgent
from ..config import BoxDefaults


class Box(PortrayedAgent) :

    def __init__(self,
                 unique_id : int,
                 model : Model,
                 **kwargs : int) :
        super(Box, self).__init__(unique_id, model)
        self.weight       = kwargs.get("weight", BoxDefaults.BASE_WEIGHT.value)
        self.noise_weight = kwargs.get("noise_weight", BoxDefaults.NOISE_WEIGHT.value)

        if self.noise_weight :
            self.weight = self.model.random.randint(int(0.8 * self.weight), int(1.2 * self.weight))

    def portray(self) -> Dict[str, Union[str, float]] :
        return {
            "Shape"  : "rect",
            "Filled" : "true",
            "w"      : 0.6,
            "h"      : 0.6,
            "Layer"  : 0,
            "Color"  : "#EFAD06"
        }

    def step(self) -> None :
        pass
