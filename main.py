from copyreg import constructor
from io import BytesIO
from urllib import request
from xmlrpc.server import SimpleXMLRPCDispatcher
import bs4, requests, webbrowser
from PIL import Image

#for id in range(10):
 #   if id == 0: continue
  
  #  requestId = str(id).zfill(3)
 

#    res = requests.get(f'https://www.serebii.net/pokedex-swsh/icon/{requestId}.png')

 
 #   img = Image.open(BytesIO(res.content))
  #  img.save(f'data/icons/{requestId}.png')


res = requests.get('https://www.serebii.net/pokedex-swsh/')

data = bs4.BeautifulSoup(res.text, 'html.parser')

selectedData = data.select('form[name="nav"] > select > option')

#for option in selectedData:
 #   print(option.getText())

#f = open("pokedex.txt", 'w')
#f.write(pokeListText)
#f.close()

poke = selectedData[146]['value']

res = requests.get(f'https://www.serebii.net{poke}')

pokemon = bs4.BeautifulSoup(res.text, 'html.parser')
pokeData = pokemon.select('table.dextable')

pokeName = pokeData[1].select('td.fooinfo')[0].getText()
pokeID = pokeData[1].select('td.fooinfo')[2].select('table > tr > td')[1].getText()
pokeTypes = []
pokeTypesData = pokeData[1].select('td.cen > a > img')

for type in pokeTypesData:
    pokeTypes.append(type['alt'])

pokeCaptureRate = pokeData[1].select('td.fooinfo')[7].getText()
pokeLocationsData = pokeData[6].select('tr')

def parseLocationData(pokeLocationsData): 
    dlcFlag = 0
    pokeLocations = []

    for location in pokeLocationsData:
        if (len(location.select('td')) < 2) : continue
        versions = location.select('td')[0].getText()

        if dlcFlag > 0:
            if dlcFlag == 1: dlcName = 'Isle of Armor'
            if dlcFlag == 2: dlcName = 'Crown Tundra'
            versions = dlcName + ' ' + versions
            
            dlcFlag = 0

        if (versions == 'Crown Tundra') or (versions == 'Isle of Armor'):
            if(versions == 'Isle of Armor'): dlcFlag = 1
            if(versions == 'Crown Tundra'): dlcFlag = 2

            versions = location.select('td')[0].getText() + ' ' + location.select('td')[1].getText()
            locations = location.select('td')[2].getText()

            pokeLocations.append({ 'versions' : versions, 'location' : locations })
            continue

        locations = location.select('td')[1].getText()

        pokeLocations.append({ 'versions' : versions, 'location' : locations })

    return pokeLocations

print (parseLocationData(pokeLocationsData))