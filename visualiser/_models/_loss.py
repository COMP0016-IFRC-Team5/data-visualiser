from enum import Enum

__all__ = ["Loss"]


class Loss(Enum):
    deaths = "Deaths"
    affected_people = "Affected People"
