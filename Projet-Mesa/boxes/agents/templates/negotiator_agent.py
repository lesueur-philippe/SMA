from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Union

from mesa import Model

from boxes.agents.config import AgentDefaults
from boxes.agents.portrayed_agent import PortrayedAgent
from boxes.agents.props.boxes import Box
from boxes.utils.types import Position


class NegotiatorAgent(PortrayedAgent, ABC) :

    @abstractmethod
    def ask(self, other : NegotiatorAgent, request : Position) :
        """
        Ask a second agent about a given position.
        :param other:
        :param request:
        :return:
        """
        pass

    @abstractmethod
    def answer(self, request : Position) :
        pass


