from __future__ import annotations
from mesa import Model

from typing import List, Optional

from . import Box
from .negotiation import Message, Status
from .templates import BaseAgent, NegotiatorAgent
from ..models.box_model import BoxModel
from ..utils.types import Position
from ..utils import get_distance


class NegotiatingAgent(BaseAgent, NegotiatorAgent) :

    def __init__(self,
                 unique_id : int,
                 model     : BoxModel,
                 **kwargs  : float) :

        super(NegotiatingAgent, self).__init__(unique_id, model, **kwargs)

        self.decided     : bool = False

        self.target_box  : Optional[Box]      = None
        self.carried_box : Optional[Box]      = None
        self.target_pos  : Optional[Position] = None
        self.chosen_pos  : Optional[Position] = None

        self.possible_steps     : Optional[List[Position]] = None
        self.distance_to_target : Optional[int] = None

    def _pickup_box(self, box : Box) -> None :
        super(NegotiatingAgent, self)._pickup_box(box)
        print("Pickup !")
        self.target_pos = self.model.platform_pos
        self.carried_box = box
        print(self.carrying, self.currently_carrying, self.target_pos, self.target_box)

    def _drop_box(self) -> None :
        super(NegotiatingAgent, self)._drop_box()
        self.carried_box = None
        self.target_pos = None
        self.target_box = None

    def _move(self) -> None :
        self.model.grid.move_agent(self, self.chosen_pos)

    def _find_best_move(self) -> None :
        # Fill possible steps if needed
        if not self.possible_steps :
            self.compute_possible_steps()

        # Retrieve agent list
        agents = [agent for agent in self.model.agent_list if agent != self]

        # Loop while not step has been decided
        while len(self.possible_steps) > 0 and not self.chosen_pos :
            test_pos = self.possible_steps[0]

            # Ask other agents about this position
            self.ask(agents, test_pos)

        # If no step was chosen, stay there
        if self.chosen_pos is None :
            self.chosen_pos = self.pos

        self.decided = True

    def assign_box(self, box : Box) :
        self.target_box = box
        self.target_pos = box.pos
        self.distance_to_target = get_distance(self.pos, self.target_pos)

    def step(self) -> None :
        # Find best move
        self._find_best_move()

        # Move
        self._move()

        # Act on surroundings
        neighbouring_cells = self.model.grid.get_neighborhood(
                self.pos, moore = False, include_center = False
        )
        # close_agents = self.model.grid.get_cell_list_contents(neighbouring_cells)

        # print(f"{neighbouring_cells}\n{self.target_pos}")
        if not self.carrying and self.target_pos in neighbouring_cells :
            # print("Case 1")
            self._pickup_box(self.target_box)
        elif self.carrying and self.model.platform_pos in neighbouring_cells :
            # print("Case 2")
            self._drop_box()

    def ask(self, targets : List[NegotiatorAgent], position : Position) :

        # Send first call for approval about position
        cfa = Message(Status.ASK, f"{position}")
        replies = self.send(cfa, targets)

        # Filter out "positive" replies (aka agreeing agents)
        replies = [rep for rep in replies if rep.status != Status.AGREE]
        senders = [msg.source for msg in replies]

        if len(replies) > 0 :
            # Possible cases : Discuss or Refuse
            # If there is a refuse, must retract
            # If there is no refuse, then discuss
            received_refusal = any([msg.status == Status.REFUSE for msg in replies])

            if received_refusal :
                answer = self._handle_refuse(position)
            else :
                answer = self._handle_discuss(position, replies)

            self.send(answer, senders)
        else :
            self.chosen_pos = position

    def reply(self, message : Message) -> Optional[Message] :
        position : Position = eval(message.message)
        reply : Optional[Message] = None
        # Possible cases : Ask, confirm or retract
        if message.status == Status.ASK :
            reply = self._handle_ask(position, message.source)
        elif message.status == Status.CONFIRM :
            self._handle_confirm(position)
        elif message.status == Status.RETRACT :
            self._handle_retract()

        return reply

    def _handle_ask(self, position : Position, sender : NegotiatingAgent) -> Message :
        # Compute possible steps if needed
        if not self.possible_steps :
            self.compute_possible_steps()

        if len(self.possible_steps) > 0 :
            best_pos = self.possible_steps[0]
        else :
            best_pos = self.pos

        same_pos = best_pos == position

        if not same_pos :
            msg = Message(Status.AGREE)
        else :
            status  = Status.REFUSE if self.decided else Status.DISCUSS
            content = f"{self.distance_to_target}" if not self.decided else None
            msg = Message(status, content)

        msg.source = self
        msg.target = sender
        return msg

    def _handle_agree(self) :
        pass

    def _handle_refuse(self, position : Position) -> Message :

        # Remove position from possible steps
        self._remove_position(position)

        # Generate messages
        return Message(Status.RETRACT)

    def _handle_discuss(self, position : Position, messages : List[Message]) -> Message :

        # Find out if self is closer than all the other agents
        closer = all([self.distance_to_target <= eval(msg.message) for msg in messages])

        if closer :
            # Confirm position to all agents
            self.chosen_pos = position
            return Message(Status.CONFIRM, f"{position}")
        else :
            # Someone else is closer - Retract position
            self._remove_position(position)
            return Message(Status.RETRACT)

    def _handle_retract(self) :
        pass

    def _handle_confirm(self, position : Position) :
        # Remove the position from available steps
        self._remove_position(position)

    def compute_possible_steps(self) :
        self.possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore = False, include_center = False
        )
        self.possible_steps = sorted(self.possible_steps, key = lambda pos : get_distance(pos, self.target_pos))

    def _remove_position(self, position) :
        self.possible_steps = [pos for pos in self.possible_steps if pos != position]
        self.possible_steps = sorted(self.possible_steps, key = lambda pos : get_distance(pos, self.target_pos))
