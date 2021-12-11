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
        if not self.possible_steps :
            self.possible_steps = self.model.grid.get_neighborhood(
                    self.pos, moore = False, include_center = False
            )
            self.possible_steps = sorted(self.possible_steps, key = lambda pos : get_distance(pos, self.target_pos))

        agents = self.model.agents

        while len(self.possible_steps) > 0 and not self.chosen_pos :
            test_pos = self.possible_steps[0]

            # Ask other agents about this position
            chosen = self.ask(agents, test_pos)

            if chosen :
                self.chosen_pos = self.possible_steps[0]

        if self.chosen_pos is None :
            self.chosen_pos = self.pos

        self.decided = True

    def assign_box(self, box : Box) :
        self.target_box = box
        self.target_pos = box.pos
        self.distance_to_target = get_distance(self.pos, self.target_pos)

    def step(self) -> None :
        # print("Step !", self)
        # Move
        self._move()

        # Act on neighbours
        neighbours = self.model.grid.get_neighborhood(
                self.pos, moore = False, include_center = False
        )
        close_agents = self.model.grid.get_cell_list_contents(neighbours)

        print(f"{neighbours}\n{self.target_pos}")
        if not self.carrying and self.target_pos in neighbours :
            print("Case 1")
            self._pickup_box(self.target_box)
        elif self.carrying and self.model.platform_pos in neighbours :
            print("Case 2")
            self._drop_box()

    def ask(self, targets : List[NegotiatorAgent], position : Position) -> bool :

        # Send first call for approval about position
        cfa = Message(Status.ASK, f"{position}")
        replies = self.send(cfa, targets)

    def reply(self, message : Message) -> Optional[Message] :
        pass

    def _handle_ask(self, position : Position) -> Message :
        if not self.possible_steps :
            self.possible_steps = self.model.grid.get_neighborhood(
                    self.pos, moore = False, include_center = False
            )
            self.possible_steps = sorted(self.possible_steps, key = lambda pos : get_distance(pos, self.target_pos))

        best_pos = self.possible_steps[0]
        same_pos = best_pos == position

        if not same_pos :
            return Message(Status.AGREE)
        else :
            status  = Status.REFUSE if self.decided else Status.DISCUSS
            content = f"{self.distance_to_target}" if not self.decided else None
            return Message(status, content)

    def _handle_agree(self) :
        pass

    def _handle_refuse(self, position : Position, agents : List[NegotiatorAgent]) -> List[Message] :

        # Remove position from possible steps
        self.possible_steps = [pos for pos in self.possible_steps if pos != position]
        self.possible_steps = sorted(self.possible_steps, key = lambda pos : get_distance(pos, self.target_pos))

        # Generate messages
        return [Message(Status.RETRACT)] * len(agents)

    def _handle_discuss(self, position : Position, agents : List[NegotiatorAgent]) -> List[Message] :
        pass
