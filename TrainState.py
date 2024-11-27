from enum import Enum

class TrainState(Enum):
    UNKNOWN = 0
    STOPPED = 1
    WAITING = 2
    SLOWING = 3
    MOVING = 4