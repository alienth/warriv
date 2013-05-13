import json
import requests

RegionUS = { 'name': 'Americas',
             'url':  'http://us.battle.net/',
           }

RegionEU = { 'name': 'Europe',
             'url':  'http://eu.battle.net/',
           }

RegionAS = { 'name': 'Asia',
             'url':  'http://as.battle.net/',
           }

AllRegions = [RegionUS, RegionEU, RegionAS]

def battle_id(battletag):
    return battletag.replace('#', '-')

# Returns the career from the requested region.
# If no region is requested, returns the career most used. (NYI, TODO)
def get_career(battletag, region = RegionUS):
    id = battle_id(battletag)

    url = '%s/api/d3/profile/%s/' % (region['url'], id)

    req = requests.get(url)

    if req.status_code == 200:
        data = json.loads(req.text)
        return Career(data)
    elif req.status_code == 404:
        raise IOError('career not found')
    else:
        raise IOError('error accessing api')



def get_all_careers(battletag):

    careers = []
    for region in AllRegions:
        careers.append(get_career(battletag))

    return careers


class Career(object):

    def __init__(self, data):
        self.data = data

    # For just one day
    def heroes(self):
        heroes = []
        for herodata in self.data['heroes']:
            heroes.append(Hero(herodata))

        return heroes

class Hero(object):

    def __init__(self, data):
        self.data = data
        self.name = data['name']
