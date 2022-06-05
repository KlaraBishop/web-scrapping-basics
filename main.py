from io import BytesIO
import bs4, requests, json
from PIL import Image

# Parses the alt values from an array of image elements, returns an array of strings
def parseTypeData(pokeTypesData):
    pokeTypes = []

    for type in pokeTypesData:
        pokeTypes.append(type['alt'])

    return pokeTypes

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

# gets the icon of a pokemon given an int ID of the desired pokemon
def getPokeIcons(pokeID):
    requestId = str(pokeID).zfill(3)
 
    res = requests.get(f'https://www.serebii.net/pokedex-swsh/icon/{requestId}.png')
 
    img = Image.open(BytesIO(res.content))
    img.save(f'data/icons/{requestId}.png')

# helper function that returns an array of values to append to a URL to get needed data
# TODO add a mode variable that lets the user determine which pokedex to get
# Currently only gets values for the kanto dex
def getPokedexURLS():
    pokeArray = []

    res = requests.get('https://www.serebii.net/pokedex-swsh/')

    data = bs4.BeautifulSoup(res.text, 'html.parser')

    selectedData = data.select('form[name="nav"] > select > option')

    for value in selectedData:
        pokeArray.append(value['value'])

    return pokeArray

def getPokemonData(idRange):
    pokedexURLS = getPokedexURLS()
    pokedex = []

    for x in range(1, idRange + 1):
        res = requests.get(f'https://www.serebii.net{pokedexURLS[x]}')

        pokemon = bs4.BeautifulSoup(res.text, 'html.parser')
        pokeData = pokemon.select('table.dextable')
        pokeLocationsData = pokeData[6].select('tr')

        pokeName = pokeData[1].select('td.fooinfo')[0].getText()
        pokeID = pokeData[1].select('td.fooinfo')[2].select('table > tr > td')[1].getText()
        pokeCaptureRate = pokeData[1].select('td.fooinfo')[7].getText()
        pokeTypes = parseTypeData(pokeData[1].select('td.cen > a > img'))
        pokeLocations = parseLocationData(pokeLocationsData)

        pokemonObj = { 'id' : pokeID, 'name' : pokeName, 'capture-rate' : pokeCaptureRate, 'types' : pokeTypes, 'locations' :  pokeLocations}
        pokedex.append(pokemonObj)

    return pokedex

pokedex = getPokemonData(9)

f = open("pokedex.json", 'w')
f.write(json.dumps(pokedex))
f.close()