from typing import Dict, Union

from ..agents import PortrayedAgent


def agent_portrayal(agent : PortrayedAgent) -> Dict[str, Union[str, float]]:
    return agent.portray()
