import numpy as np

from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement


def agent_portrayal(agent : Agent) :
    if isinstance(agent, BoxAgent) :
        return box_portrayal(agent)
    elif isinstance(agent, CarrierAgent) :
        return carrier_portrayal(agent)
    return destination()


def carrier_portrayal(agent : CarrierAgent) :
    portrayal = {
        "Shape"  : "rect",
        "Filled" : "true",
        "w"      : 0.8,
        "h"      : 0.8,
        "Layer"  : 0
    }
    if not agent.carrying :
        color = "#A0B8CF"
    else :
        color = "#EFAD06"
    portrayal["Color"] = color
    return portrayal


def box_portrayal(box : BoxAgent) :
    portrayal = {
        "Shape"  : "rect",
        "Filled" : "true",
        "w"      : 0.6,
        "h"      : 0.6,
        "Layer"  : 0,
        "Color"  : "#EFAD06"
    }

    return portrayal


def destination() :
    return {
        "Shape"  : "circle",
        "Filled" : "true",
        "r"      : 0.8,
        "Layer"  : 0,
        "Color"  : "#EF767A"
    }


chart = ChartModule([{"Label" : "Number of carrying agents",
                      "Color" : "Black"},
                     {"Label" : "Remaining boxes",
                      "Color" : "#EFAD06"}],
                    data_collector_name = "data_collectors")

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(BoxModel,
                       [grid, chart],
                       "Box Carrying Model",
                       {"nb_agents" : 2,
                        "nb_boxes" : 2,
                        "width" : 10,
                        "height" : 10,
                        "torus" : False})
server.port = 8521
server.launch()

