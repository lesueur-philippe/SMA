import numpy as np

from .types import Position


def get_distance(from_cell : Position, to_cell : Position) -> int :
    return np.sum(np.abs(np.array(from_cell) - np.array(to_cell)))
