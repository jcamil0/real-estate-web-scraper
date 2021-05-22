# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
import sys


def getAllUrl(zone, urlid, pagination):
    for j in range(pagination):
        id = 0
        for i in zone.keys():
            baseurl = 'https://www.fincaraiz.com.co/casas/venta/{}/cali/?ad=30|{}||||1||9|||82|8200006|{}|||||||||||||||1|||1||griddate%20desc||||-1||||'.format(
                i, j, urlid[id])
            id += 1
            page = requests.get(baseurl)
            soup = BeautifulSoup(page.content, 'html.parser')
            urls = soup.find_all('div', class_='span-title')
            for items in urls:
                for x in items.find_all('a', href=True):
                    if x['href'].startswith("https") == False:
                        zone[i].append(
                            'https://www.fincaraiz.com.co{}'.format(x['href']))

        with open('./data/urls.json', 'w', encoding='utf-8') as f:
            json.dump(zone, f, ensure_ascii=False, indent=4)
        print("file urls.json created")
        print("page {} ready !!".format(j+1))


def scrapy_data(data):
    for items in zone.keys():
        data = []
        home = 1
        for x in zone[items]:
            r = requests.get(x)
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

            # estrato = soup.find("ul", {"class": "boxcube"})
            # _estrato = []

            # if estrato:
            #     newsoup = BeautifulSoup(str(estrato), 'html.parser')
            #     lis = newsoup.find_all('li')
            #     for li in lis:
            #         print(li)

            data.append(
                {
                    "title": title.text,
                    "price": prices.text.strip(),
                    "mts": mts,
                    "rooms": rooms.strip(),
                    "baths": baths.strip(),
                    "parking": parking.strip(),
                    # "interior": interiors,
                    # "Exterior": _ext,
                    # "around": _sector,
                    "url": x,
                    # "xxx": _estrato
                })
            home += 1
        # data["total"] = len(data)
        WriteData(data, items)


def WriteData(data, items):
    with open('./data/{}.json'.format(items), 'w', encoding='utf-16') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("file {}.json ready!!".format(items))


if __name__ == "__main__":
    print("recolectando datos....")
    zone = {'norte': [], 'oeste': [], 'centro': [], 'sur': [], "oriente": []}
    urlid = ["8200101", "8200102", "8200103", "8200104", "8200105"]
    data = []
    pagination = 1

    if len(sys.argv) == 1:
        getAllUrl(zone, urlid, pagination)
    else:
        pagination = int(sys.argv[1])
        getAllUrl(zone, urlid, pagination)

    scrapy_data(data)

    # drive = webdriver.Chrome(
    #     "/home/camilo/Documentos/bigdata/proyecto/page/chromedriver")
    # drive.get("http://0.0.0.0:8000/page/")

    print("bye....")
    # python -m SimpleHTTPServer 8000
