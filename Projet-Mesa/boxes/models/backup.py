## AssigningModel
def solve_conflict(self, agent1, agent2) :
    # check agent2 already negociated this step
    if not agent2.negociated and agent2.round == agent1.round :
        agent2.available_next_steps()
    a1_pos = agent1.wished_positions.copy()
    a2_pos = agent2.wished_positions.copy()
    a1p = deepcopy(agent1.pos)
    a2p = deepcopy(agent2.pos)
    for pos in a1_pos :
        if pos in a2_pos :
            # if there are enough positions available, delete one
            if len(agent1.wished_positions) > len(agent2.wished_positions) :
                agent1.wished_positions.remove(pos)
            # if there are enough positions available, delete one
            elif len(agent2.wished_positions) > len(agent1.wished_positions) :
                agent2.wished_positions.remove(pos)
            # if there are equal number of available positions
            elif len(agent1.wished_positions) == 1 and len(agent2.wished_positions) == 1 :
                if agent1.target_box is None :
                    if agent2.target_box is None :
                        agent2.wished_positions = [a2p]
                    else :
                        print(agent2.target_box)
                        print(agent2.target_box.pos)
                        if get_distance(agent2.target_pos, a1p) < get_distance(agent2.target_pos, a2p) :
                            if get_distance(a1p, a2p) == 1 :
                                agent1.wished_positions = [a2p]
                                agent2.wished_positions = [a1p]
                            else :
                                agent1.wished_positions = [a1p]
                elif agent2.target_box is None :
                    if agent1.target_box is None :
                        agent1.wished_positions = [a1p]
                    else :
                        if get_distance(agent1.target_pos, a2p) < get_distance(agent1.target_pos, a1p) :
                            if get_distance(a2p, a1p) == 1 :
                                agent1.wished_positions = [a2p]
                                agent2.wished_positions = [a1p]
                            else :
                                agent2.wished_positions = [a2p]

    agent1.negociated = True
    agent1.negociated_with.append(agent2)
    agent2.negociated = True
    agent2.negociated_with.append(agent1)





