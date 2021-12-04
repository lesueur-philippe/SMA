from mesa import Model


def get_nb_carrying(model : Model) :
    return sum([1 if agent.carrying else 0
                for agent in model.carriers.values()])


def get_remaining_boxes(model : Model) :
    return len(model.boxes.values())

