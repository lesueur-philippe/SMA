from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from typing import Dict, Union

from boxes.agents import PortrayedAgent
from boxes.models import AssigningModel, SimpleModel


def agent_portrayal(agent : PortrayedAgent) -> Dict[str, Union[str, float]]:
    return agent.portray()


chart = ChartModule([{"Label" : "Carrying",
                      "Color" : "Black"},
                     {"Label" : "Boxes",
                      "Color" : "#EFAD06"}],
                    data_collector_name = "data_collectors")

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(AssigningModel,
                       [grid, chart],
                       "Box Carrying Model",
                       {"nb_agents" : 2,
                        "nb_boxes" : 6,
                        "width" : 10,
                        "height" : 10,
                        "torus" : False})
server.port = 8521
server.launch()

