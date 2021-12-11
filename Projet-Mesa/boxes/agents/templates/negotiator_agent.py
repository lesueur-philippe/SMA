from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from boxes.agents.negotiation import Message
from boxes.agents.portrayed_agent import PortrayedAgent
from boxes.utils.types import Position


class NegotiatorAgent(PortrayedAgent, ABC) :

    def send(self, message : Message, targets : List[NegotiatorAgent]) -> List[Message] :
        """
        Sends a message to other agents and returns the replies

        :param message: the message to send
        :param targets: the target for the message
        :return: the list of replies
        """

        replies = []
        for target in targets :
            message.source = self
            message.target = target
            replies.append(target.reply(message))

        return list(filter(None, replies))

    @abstractmethod
    def ask(self, targets : List[NegotiatorAgent], position : Position) -> bool :
        """
        Asks targets agents about a position and returns whether the position is chosen.

        :param targets: the agents to send the position to
        :param position: the position to enquire about
        :return: whether the position is chosen or not
        """
        pass

    @abstractmethod
    def reply(self, message : Message) -> Optional[Message] :
        pass
