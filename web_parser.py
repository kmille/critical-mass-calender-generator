import requests
from bs4 import BeautifulSoup
from ipdb import set_trace
import re
import os
import json

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
c = []
for city in os.listdir("html/"):
    #get_details(city['name'], city['url'])
    c.append(get_details(city, city))
print(json.dumps(c))
