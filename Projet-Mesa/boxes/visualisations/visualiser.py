from __future__ import annotations

from typing import Dict, List

from mesa import Model
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement


class Visualiser :

    def __init__(self) :
        self.port  : int = None
        self.title : str = None
        self.model : Model = None
        self.params : Dict = {}
        self.vis_elements : List = []
        self.open_browser : bool = False

    def set_port(self, port : int) -> Visualiser:
        self.port = port
        return self

    def set_title(self, title : str) -> Visualiser :
        self.title = title
        return self

    def set_model(self, model : Model) -> Visualiser :
        self.model = model
        return self

    def set_model_params(self, params : Dict) -> Visualiser :
        self.params = params
        return self

    def set_open_browser(self, flag : bool) -> Visualiser :
        self.open_browser = flag
        return self

    def add_vis_element(self, element : VisualizationElement) -> Visualiser :
        self.vis_elements.append(element)
        return self

    def add_vis_elements(self, elements : List[VisualizationElement]) -> Visualiser :
        self.vis_elements += elements
        return self

    def run(self) :
        server = ModularServer(self.model,
                               self.vis_elements,
                               self.title,
                               self.params)
        server.launch(self.port, self.open_browser)

