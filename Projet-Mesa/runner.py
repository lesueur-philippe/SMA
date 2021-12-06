from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from typing import Dict, Union

from boxes.models import AssigningModel, SimpleModel

from boxes.visualisations import agent_portrayal, Visualiser


def main() :
    grid_height = 20
    grid_width = 20
    nb_agents = 6
    nb_boxes = 10

    chart = ChartModule([{"Label" : "Carrying",
                          "Color" : "Black"},
                         {"Label" : "Boxes",
                          "Color" : "#EFAD06"}],
                        data_collector_name = "data_collectors")

    grid = CanvasGrid(portrayal_method = agent_portrayal,
                      grid_width = grid_width,
                      grid_height = grid_height,
                      canvas_width = 500,
                      canvas_height = 500)

    params = {"nb_agents" : nb_agents,
              "nb_boxes"  : nb_boxes,
              "width"     : grid_width,
              "height"    : grid_height,
              "torus"     : False}

    visualiser = Visualiser()
    visualiser = visualiser.set_port(8521)\
                           .set_model(AssigningModel)\
                           .set_title("Box Model Simulation")\
                           .add_vis_elements([grid, chart])\
                           .set_model_params(params)\
                           .set_open_browser(False)

    visualiser.run()


if __name__ == '__main__' :
    main()
