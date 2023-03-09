from enum import Enum

__all__ = ["Loss"]


class Loss(Enum):
    """An enumeration of types of losses.

    Each member of the enumeration represents a different type of loss.

    """
    deaths = "Deaths"
    affected_people = "Affected People"

    def __eq__(self, other):
        """Check if two Losses have the same value.

        Args:
            other (Loss): The other Loss to compare against.

        Returns:
            bool: True if the Losses have the same value; False otherwise.

        """
        return self.value == other.value
