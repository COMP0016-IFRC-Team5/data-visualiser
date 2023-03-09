import visualiser

if __name__ == '__main__':
    visualiser.set_data_folder('./data')
    print(visualiser.get_available_countries())
    countries = ["Albania", "Pakistan"]
    # country = "Mexico"
    # country = "Belize"
    events = ["Floods",
              "eArthQuaKEs"]  # case insensitive
    # event = 'Floods'
    # event = 'Storms'
    visualiser.plot_exceedance_curves(
        countries,
        events,
        [visualiser.Loss.deaths, visualiser.Loss.affected_people],
        15
    )
    #visualiser.plot_exceedance_curves(country, event,
    #                                  visualiser.Loss.deaths, 15)
    #table = visualiser.get_exceedance_table(country, event, 15)
    tables = visualiser.get_exceedance_table(countries, events,15)
    for _country in tables:
        for _event in tables[_country]:
            df = tables[_country][_event]
            print(_country, _event)
            print(df)
            print("--------------------")
