import requests
from bs4 import BeautifulSoup
from ipdb import set_trace
import re
import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR

session = requests.Session()

base = "http://criticalmass.de/"

def get_cities():
    resp = session.get(base)
    bs = BeautifulSoup(resp.content.decode(), 'html.parser')
    select = bs.find('select')
    cities = []
    for option in select.findAll('option'):
        try:
            #set_trace()
            city = {}
            city['name'] = option.contents[0].strip()
            city['url'] = option.attrs['value']
            cities.append(city)
            #print(city)
        except AttributeError as e:
            print("Error parsing cities", e)
    #print(cities)
    return cities


def get_details(name, url):
    #print("Parsing city '%s'" % name)
    #resp = session.get(base + url)
    with open("html/%s" % url, "r") as f:
        html = f.read()
    if "Leider haben wir zur Zeit nicht genug Daten über Critical Mass " in html:
        return
    bs = BeautifulSoup(html, 'html.parser')
    details = {}
    details['name'] = name
    details['url'] = url
    desc  = "\n".join([t.text.strip() for t in bs.findAll(class_="panel-body")])
    details['description'] = desc
    try:
        url_text = bs.find(class_='list-unstyled').text.strip()
        urls  = "\n".join([u.strip() for u in url_text.splitlines() if 'Likes' not in u])
        details['urls'] = urls
        #print(details)
    except AttributeError as e :
        pass
        # no urls
    return details

#cities = get_cities()
#get_details('Darmstadt', 'erlangen.html')
#exit()
def generate_json():
    c = []
    for city in os.listdir("html/"):
        #get_details(city['name'], city['url'])
        detail = get_details(city, city)
        if detail:
            c.append(detail)
    print(json.dumps(c))

def find_day(desc):
    for i in range(5):
        print(datetime.today()+ relativedelta(months=i))
    print("")
    for i in range(5):
        print(datetime.today()+ relativedelta(months=i) + relativedelta(weekday=FR(-1)))
    #return datetime.now() + relativedelta(weekday=FR(-1))

def main():
    critical_masses = json.load(open("aktueller_stand.json"))
    for mass in critical_masses[1:]:
        desc = mass['description']
        print(desc)
        date = find_day(desc)
        print(date)
        exit()



if __name__ == '__main__':
    main()
