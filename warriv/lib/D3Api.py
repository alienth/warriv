import json
import requests

RegionUS = { 'name': 'Americas',
             'url':  'http://us.battle.net/',
           }

RegionEU = { 'name': 'Europe',
             'url':  'http://eu.battle.net/',
           }

RegionAS = { 'name': 'Asia',
             'url':  'http://kr.battle.net/',
           }

AllRegions = [RegionUS, RegionEU, RegionAS]

def battle_id(battletag):
    return battletag.replace('#', '-')

# Returns the career from the requested region.
# If no region is requested, returns the career most used. (NYI, TODO)
def get_career(battletag, region = RegionUS):

    url = '%s/api/d3/profile/%s/' % (region['url'], battle_id(battletag))

    req = requests.get(url)

    if req.status_code == 200:
        data = json.loads(req.text)

        if 'code' in data:
            if data['code'] == 'NOTFOUND':
                return None

        return Career(data, region)
    elif req.status_code == 404:
        raise IOError('career not found')
    else:
        raise IOError('error accessing api')



def get_all_careers(battletag):

    careers = []
    for region in AllRegions:
        career = get_career(battletag, region=region)
        if career:
            careers.append(career)

    return AllCareers(careers)


class AllCareers(object):

    def __init__(self, careers):
        self.careers = careers

        heroes = []
        for career in self.careers:
              heroes = heroes + career.heroes

        self.heroes = heroes

class Career(object):

    def __init__(self, data, region):
        self.data = data
        self.region = region

        heroes = []
        for herodata in self.data['heroes']:
            heroes.append(Hero(herodata, self.region))

        self.heroes = heroes

class Hero(object):

    hardcore = False

    def __init__(self, data, region):
        self.data = data
        self.name = data['name']
        self.id = data['id']
        self.last_updated = data['last-updated']

        if data['hardcore']:
            self.hardcore = True

        self.region = region
