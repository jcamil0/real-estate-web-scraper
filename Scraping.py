from bs4 import BeautifulSoup
import requests
import json
import pandas as pd 

zone=['norte','sur','oeste','oriente',]
data={}
aux=[]
urlLists =[]

baseurl ='https://www.fincaraiz.com.co/casas/venta/{}/cali/'.format(zone[0])
page =requests.get(baseurl)
soup=BeautifulSoup(page.content, 'html.parser')

urls=soup.find_all('div',class_='span-title')
for items in urls:
    for x in items.find_all('a',href=True):
        if x['href'].startswith("https") == False:
            urlLists.append('https://www.fincaraiz.com.co{}'.format(x['href']))


def scrapy_data():
    url=0
    for items in urlLists:
        r =requests.get(items)
        soup = BeautifulSoup(r.content,'html.parser')

        title=soup.find('span', {'style':'font-weight:normal'}).text.strip()
        prices=soup.find('div' , {'class':'price'}).text.strip()
        mts=soup.find('span',{'class':'advertSurface'}).text.strip()
        rooms=str(soup.find('span',{'class':'advertRooms'}).text).replace("Habitaciones:","")
        baths=str(soup.find('span',{'class':'advertBaths'}).text).replace("Baños:","")
        parking=str(soup.find('span',{'class':'advertGarages'}).text).replace("Parqueaderos:","")


        interior=soup.find("ul", {"id":"tblInitialInteriores"})
        _interior=[]
        if interior:
            newsoup = BeautifulSoup(str(interior), 'html.parser')
            lis = newsoup.find_all('li')
            for li in lis:
                _interior.append(li.text)            


        

        ext=soup.find("ul", {"id":"tblInitialExteriores"})
        _ext=[]
        if ext:
            newsoup = BeautifulSoup(str(ext), 'html.parser')
            lis = newsoup.find_all('li')
            for li in lis:
                _ext.append(li.text)
     

        sector=soup.find("ul", {"id":"tblInitialdelSector"})
        _sector=[]
        if sector:
                newsoup = BeautifulSoup(str(sector), 'html.parser')
                lis = newsoup.find_all('li')
                for li in lis:
                    _sector.append(li.text)
     
        aux.append({"title":title,
        "price":prices,
        "mts":mts,
        "rooms":rooms.strip(),
        "baths":baths.strip(),
        "parking":parking.strip(),
        "url":urlLists[url],
        "interior":_interior,
        "Exterior":_ext,
        "around":_sector
        })
        data["properties"]=aux
        data["total"]=len(aux)

        url+=1
        if url==10:
            break
    

if __name__ =="__main__":
    print("recolectando datos....")
    scrapy_data()


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    print("se ha creado el archivo data.json")
    


