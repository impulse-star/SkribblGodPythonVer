from enum import Enum


class Status(Enum):
    Drawing = 1
    Guessing = 2
    Idle = 3
    NotPlaying = 4
    BetweenRounds = 5
