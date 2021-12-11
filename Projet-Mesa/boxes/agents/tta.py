from __future__ import annotations

from typing import List

from boxes.agents.negotiation import Message, Status


class AA :

    def __init__(self, x, y, dec, dis) :
        self.position = (x, y)
        self.decided = dec
        self.distance = dis

    def send(self, msg : Message, dests : List[AA]) :
        replies = []
        for dest in dests :
            msg.source = self
            msg.target = dest
            replies.append(dest.reply(msg))

        return replies

    def ask(self, others : List[AA]) :
        m = Message(Status.ASK, f"{self.position}")
        reps = self.send(m, others)

        pos = [rep for rep in reps if rep.status == Status.AGREE]
        neg = [rep for rep in reps if rep.status != Status.AGREE]

        print(pos)
        print(neg)

        if len(neg) > 0 :
            # Negative replies
            # Check if refused
            refused = any([msg.status == Status.REFUSE for msg in neg])
            d = [msg.source for msg in neg]
            print(f"Ref : {refused}")
            if refused :
                m = Message(Status.RETRACT, "")
                self.send(m, d)
            else :
                closer = all([self.distance <= eval(msg.message) for msg in neg])

                sts = Status.CONFIRM if closer else Status.RETRACT
                cnt = f"{self.position}" if closer else ""
                m = Message(sts, cnt)

                self.send(m, d)

    def reply(self, message : Message) :

        if message.status == Status.ASK :
            if self.position == eval(message.message) :
                return Message(Status.REFUSE, "", self, message.source) if self.decided \
                    else Message(Status.DISCUSS, f"{self.distance}", self, message.source)
            else :
                return Message(Status.AGREE, "", self, message.source)
        else :
            print(message)


def init() :

    a = AA(0, 2, False, 3)
    b = AA(3, 5, False, 4)
    c = AA(3, 5, False, 2)
    d = AA(3, 5, False, 5)

    return a, b, c, d
