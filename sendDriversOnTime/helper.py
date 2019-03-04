import pandas as pd

def format_country_cities(cities):
    """
    Format the list of country cities to pass to the db querystring.

    :param cities: List of the cities in a country
    :type cities: list
    :return: Formatted list of cities in a country
    :rtype: str
    """
    return cities

def save_df(data, output_path):
    print('Saving data to {}'.format(output_path))
    data.to_csv(output_path)
    print('Data saved')