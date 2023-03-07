__all__ = ["CountryAdapter"]

from _utils import Directory


class CountryAdapter:
    def __init__(self, selected_folder: Directory):
        self.__selected_folder = selected_folder
        self.__countries = selected_folder.get_directories()

    @property
    def countries(self) -> list[str]:
        return list(
            map(
                lambda country: country.get_dirname(),
                self.__countries
            )
        )

    def get_country(self, country: str) -> Directory:
        return self.__selected_folder.find_directory(country)
