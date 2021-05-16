# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from selenium import webdriver
from helper_functions import clean_tweet
import time

zone = {'norte': [], 'oeste': [], 'centro': [], 'sur': [], "oriente": []}
urlid = ["8200101", "8200102", "8200103", "8200104", "8200105"]
data = []
urlLists = []


def getAllUrl():
    for j in range(1):
        for i in zone.keys():
            baseurl = 'https://www.fincaraiz.com.co/casas/venta/{}/cali/?ad=30|{}||||1||9|||82|8200006|8200101|||||||||||||||1|||1||griddate%20desc||||-1||||'.format(
                i, j)
            page = requests.get(baseurl)
            soup = BeautifulSoup(page.content, 'html.parser')
            urls = soup.find_all('div', class_='span-title')
            for items in urls:
                for x in items.find_all('a', href=True):
                    if x['href'].startswith("https") == False:
                        zone[i].append(
                            'https://www.fincaraiz.com.co{}'.format(x['href']))

            with open('./data/{}.json'.format(i), 'w', encoding='utf-8') as f:
                json.dump(zone[i], f, ensure_ascii=False, indent=4)
            print("se ha creado el archivo {}.json".format(i))


def scrapy_data():
    url = 0
    for items in zone.values():
        print(items)
        r = requests.get(items)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('div', class_='box').span
        prices = soup.find('div', {'class': 'price'})
        mts = soup.find('span', {'class': 'advertSurface'}).text.strip()
        rooms = str(soup.find('span', {'class': 'advertRooms'}).text).replace(
            "Habitaciones:", "")
        baths = str(soup.find('span', {'class': 'advertBaths'}).text).replace(
            "Baños:", "")
        parking = str(soup.find('span', {'class': 'advertGarages'}).text).replace(
            "Parqueaderos:", "")

        interior = soup.find("ul", {"id": "tblInitialInteriores"})
        interiors = []
        if interior:
            newsoup = BeautifulSoup(str(interior), 'html.parser')
            lis = newsoup.find_all('li')
            for li in lis:
                interiors.append(li.text)

        ext = soup.find("ul", {"id": "tblInitialExteriores"})
        _ext = []
        if ext:
            newsoup = BeautifulSoup(str(ext), 'html.parser')
            lis = newsoup.find_all('li')
            for li in lis:
                _ext.append(li.text)

        sector = soup.find("ul", {"id": "tblInitialdelSector"})
        _sector = []
        if sector:
            newsoup = BeautifulSoup(str(sector), 'html.parser')
            lis = newsoup.find_all('li')
            for li in lis:
                _sector.append(li.text)

        data.append({"title": title.text,
                     "price": prices.text.strip,
                     "mts": mts,
                     "rooms": rooms.strip(),
                     "baths": baths.strip(),
                     "parking": parking.strip(),
                     #  "url": urlLists[url],
                     "interior": interiors,
                     "Exterior": _ext,
                     "around": _sector
                     })
        # # url += 1
        # # if url == 10:
        # #     break
    # WriteData()


def features():
    print()


def WriteData():
    with open('/data/hola.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("se ha creado el archivo data.json")


def NorteData():
    norteDf = pd.read_json('./data/norte.json', orient='records')
    norteDf['clean_tweet'] = norteDf['price'].apply(lambda x: clean_tweet(x))
    norteDf['item'] = 'Bitcoin'
    norteDf.drop_duplicates(subset=['title'], keep='first', inplace=True)
    return norteDf


if __name__ == "__main__":
    # print("recolectando datos....")
    getAllUrl()
    # scrapy_data()
    drive = webdriver.Chrome(
        "/home/camilo/Documentos/bigdata/proyecto/page/chromedriver")
    drive.get("http://0.0.0.0:8000/page/")


# drive = webdriver.Chrome(
#     "/home/camilo/Documentos/bigdata/proyecto/page/chromedriver")
# drive.get("http://0.0.0.0:8000/page/")
# python -m SimpleHTTPServer 8000
