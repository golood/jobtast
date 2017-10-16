import requests
import json

def isSlovar(key, slovar):
    for keys in slovar.keys():
        if key in slovar[keys]:
            return True
    return False

def getKey(key, slovar):
    for keys in slovar.keys():
        if key in slovar[keys]:
            return keys
    
def getTable():
    url = 'https://job.firstvds.ru/spares.json'
    data = requests.get(url).json()

    url = 'https://job.firstvds.ru/alternatives.json'
    slovar = requests.get(url)
    slovar = json.loads((slovar.text).replace('\'', '\"'))
    slovar = slovar['alternatives']

    d = {}
    for i in slovar.keys():
        d.setdefault(i)
        d[i] = {}
        d[i].setdefault('count')
        d[i].setdefault('arrive')
        d[i].setdefault('mustbe')
        d[i]['count'] = 0
        d[i]['arrive'] = 0
        d[i]['mustbe'] = 0

    for item in data.keys():
        if isSlovar(item, slovar):
            keySlovar = getKey(item, slovar)
            d[keySlovar]['count'] += data[item]['count']
            d[keySlovar]['arrive'] += data[item]['arrive']
            d[keySlovar]['mustbe'] = max(d[keySlovar]['mustbe'],
                                          data[item]['mustbe'])
        else:
            d.setdefault(item)
            d[item] = {}
            d[item].setdefault('count')
            d[item].setdefault('arrive')
            d[item].setdefault('mustbe')
            d[item]['count'] = data[item]['count']
            d[item]['arrive'] = data[item]['arrive']
            d[item]['mustbe'] = data[item]['mustbe']

    return d

