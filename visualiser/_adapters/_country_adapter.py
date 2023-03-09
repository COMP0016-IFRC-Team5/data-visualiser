__all__ = ["CountryAdapter"]

from .._utils import Directory


class CountryAdapter:
    """A class for working with countries represented as directories.

    Attributes:
        __selected_folder (Directory): The directory representing the selected
            country.
        __countries (list[Directory]): A list of directories representing all
            available countries.

    Args:
        selected_folder (Directory): The directory representing the selected
            country.

    """
    def __init__(self, selected_folder: Directory):
        self.__selected_folder = selected_folder
        self.__countries = selected_folder.get_directories()

    @property
    def countries(self) -> list[str]:
        """list[str]: A list of the names of all available countries."""
        return list(
            map(
                lambda country: country.get_dirname(),
                self.__countries
            )
        )

    def get_country(self, country: str) -> Directory:
        """Get the directory representing a given country.

        Args:
            country (str): The name of the country to retrieve.

        Returns:
            Directory: The directory representing the given country.

        """
        return self.__selected_folder.find_directory(country)
