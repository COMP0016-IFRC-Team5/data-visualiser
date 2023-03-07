from enum import Enum
import visualiser


class Loss(Enum):
    deaths = 1
    affected_people = 2


if __name__ == '__main__':
    visualiser.set_data_folder('./data')
    print(visualiser.available_countries)
    countries = ["Lebanon", "Spain"]
    country = 'Mexico'
    events = ["Floods", "eArthQuaKEs"]  # case insensitive
    event = 'FLOODS'
    visualiser.plot_exceedance_curves(countries, events, [Loss.deaths,
                                                          Loss.affected_people])
    visualiser.plot_exceedance_curves(country, event, Loss.deaths)
    table = visualiser.get_exceedance_table(country, event)
    tables = visualiser.get_exceedance_table(countries, events)

