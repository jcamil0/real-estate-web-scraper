from bs4 import BeautifulSoup
import requests
import json
import pandas as pd 

zone=['norte','sur','oeste','oriente',]
data={}
aux=[]
urlLists =[]
nuevo=[]

baseurl ='https://www.fincaraiz.com.co/casas/venta/{}/cali/'.format(zone[0])
page =requests.get(baseurl)
soup=BeautifulSoup(page.content, 'html.parser')
urls=soup.find_all('div',class_='span-title')

for _list in urls:
    for x in _list.find_all('a',href=True):
        urlLists.append(x['href'])
# print(nuevo)

for hola in urlLists:
    if hola.startswith("https") ==False:
        nuevo.append('https://www.fincaraiz.com.co{}'.format(hola))


url=0
for items in nuevo:
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
    else: 
        print("no encontrada")

       

    ext=soup.find("ul", {"id":"tblInitialExteriores"})
    _ext=[]
    if ext:
        newsoup = BeautifulSoup(str(ext), 'html.parser')
        lis = newsoup.find_all('li')
        for li in lis:
            _ext.append(li.text)
    else:
        print("no encontrado")

    sector=soup.find("ul", {"id":"tblInitialdelSector"})
    _sector=[]
    if sector:
            newsoup = BeautifulSoup(str(sector), 'html.parser')
            lis = newsoup.find_all('li')
            for li in lis:
                _sector.append(li.text)
    else:
        print("no encontrado")
    try:
        whatsapp =str(soup.find('div',{'class':'a_options whatsapplink'}).get('onclick')).split(",")
        whatsapp[1]=whatsapp[1].replace("'","").replace(")","").replace(";","")
    except:
        whatsapp =["","sin whatsapp"]

    aux.append({"title":title,
    "price":prices,
    "mts":mts,
    "rooms":rooms.strip(),
    "baths":baths.strip(),
    "parking":parking.strip(),
    "whatsapp":whatsapp[1],
    "url":nuevo[url],
    "interior":_interior,
    "Exterior":_ext,
    "around":_sector
    })

    data["properties"]=aux
    data["total"]=len(aux)



with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    