import visualiser

if __name__ == '__main__':
    visualiser.set_data_folder('./data')
    print(visualiser.get_available_countries())
    countries = ["Albania", "Pakistan"]
    country = 'Mexico'
    events = ["Floods", "eArthQuaKEs"]  # case insensitive
    event = 'FLOODS'
    visualiser.plot_exceedance_curves(
        countries,
        events,
        [visualiser.Loss.deaths, visualiser.Loss.affected_people],
        15
    )
    visualiser.plot_exceedance_curves(country, event, visualiser.Loss.deaths)
    table = visualiser.get_exceedance_table(country, event)
    tables = visualiser.get_exceedance_table(countries, events)
