#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from ipdb import set_trace
import json

url_cities = "https://criticalmass.in/citylist"
url_base = "https://criticalmass.in{}"
output_file = "cities.json"

session = requests.Session()

def translate(wochentag):
    days = {'Montag': 'Monday',
            'Dienstag': 'Tuesday',
            'Mittwoch': 'Wednesday',
            'Donnerstag': 'Thursday',
            'Freitag': 'Friday',
            'Samstag': 'Saturday',
            'Sonntag': 'Sunday',
            'Sonnabend': 'Sunday'
            }
    return days[wochentag]

def cycle_string_to_cycle_number(cycle_string):
    if "erste" in cycle_string:
        return 0
    if "zweit" in cycle_string:
        return 1
    if "dritt" in cycle_string:
        return 2
    if "viert" in cycle_string:
        return 3
    if "letzte" in cycle_string:
        return -1
    raise "this should not happen"


def get_cities():
    cities_result = {}
    resp = session.get(url_cities)
    bs = BeautifulSoup(resp.text, 'html.parser')
    cities_table = bs.find("table", {'id':'city-list-table'})
    cities_dirty =  cities_table.findAll('tr')[1:] # dismiss table header
    # add name, url, date_as_string
    for city in cities_dirty:
        columns = city.findAll("td")
        name = columns[0].text.strip()
        print("doing", name)
        date_as_string = " ".join(columns[2].text.split())
        if date_as_string == "":
            print(" no date found")
            continue
        cycle_string, day, __, begin, = date_as_string.split()[1:5]
        url = city.find("a")['href']
        cities_result[name] = {'url': url_base.format(url),
                               'day': translate(day),
                               'begin': begin,
                               'cycle': cycle_string_to_cycle_number(cycle_string)
                               }

    # add place of mass
    for name, city in cities_result.items():
        resp = session.get(city['url'])
        bs = BeautifulSoup(resp.text, 'html.parser')
        try:
            place = bs.findAll("dl")[2].find("dd").text
        except (AttributeError, IndexError):
            place = "" # no place found on the website
        cities_result[name].update({'location': place})
    print("Write data to {}".format(output_file))
    with open(output_file, "w") as f:
        json.dump(cities_result, f)

def main():
    get_cities()

if __name__ == '__main__':
    main()
