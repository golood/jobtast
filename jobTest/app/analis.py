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
    for i in data.keys():
        if isSlovar(i, slovar):
            keySlovar = getKey(i, slovar)
            if keySlovar in d.keys():
                d[keySlovar]['count'] += data[i]['count']
                d[keySlovar]['arrive'] += data[i]['arrive']
                d[keySlovar]['mustbe'] = max(d[keySlovar]['mustbe'],
                                               data[i]['mustbe'])
            else:
                d.setdefault(keySlovar)
                d[keySlovar] = {}
                d[keySlovar].setdefault('count')
                d[keySlovar].setdefault('arrive')
                d[keySlovar].setdefault('mustbe')
                d[keySlovar]['count'] = data[i]['count']
                d[keySlovar]['arrive'] = data[i]['arrive']
                d[keySlovar]['mustbe'] = data[i]['mustbe']
        else:
            d.setdefault(i)
            d[i] = {}
            d[i].setdefault('count')
            d[i].setdefault('arrive')
            d[i].setdefault('mustbe')
            d[i]['count'] = data[i]['count']
            d[i]['arrive'] = data[i]['arrive']
            d[i]['mustbe'] = data[i]['mustbe']


    return d

