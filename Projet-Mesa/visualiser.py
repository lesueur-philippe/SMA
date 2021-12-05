from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from typing import Dict, Union

from boxes.agents import PortrayedAgent, SmartAgent
from boxes.models import AssigningModel, SimpleModel


def agent_portrayal(agent : SmartAgent) -> Dict[str, Union[str, float]]:
    return agent.portray()


chart = ChartModule([{"Label" : "Carrying",
                      "Color" : "Black"},
                     {"Label" : "Boxes",
                      "Color" : "#EFAD06"}],
                    data_collector_name = "data_collectors")

N = 20
M = 20

grid = CanvasGrid(agent_portrayal, N, M, 500, 500)

server = ModularServer(AssigningModel,
                       [grid, chart],
                       "Box Carrying Model",
                       {"nb_agents" : 6,
                        "nb_boxes" : 10,
                        "width" : N,
                        "height" : M,
                        "torus" : False})
server.port = 8521
server.launch()

