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
        print(newsoup)
        lis = newsoup.find_all('li')
        for li in lis:
            print(li.text)
            _interior.append(li.text)
            
            print()
            print(_interior) 
    else: 
        print("no encontrada")

       

    # for ul in interior:
    #     newsoup = BeautifulSoup(str(ul), 'html.parser')
    #     lis = newsoup.find_all('li')
    #     for li in lis:
    #         print(li.text)

    # ext=soup.find("ul", {"id":"tblInitialInteriores"})
    # for ul in ext:
    #     newsoup = BeautifulSoup(str(ul), 'html.parser')
    #     lis = newsoup.find_all('li')
    #     for li in lis:
    #         print(li.text)

    # sector=soup.find("ul", {"id":"tblInitialdelSector"})
    # for ul in sector:
    #         newsoup = BeautifulSoup(str(ul), 'html.parser')
    #         lis = newsoup.find_all('li')
    #         for li in lis:
    #             print(li.text)

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
    # "Exterior":versiones_plone,
    # "around":versiones
    })

    data["properties"]=aux
    url+=1
    if url == 4 :
        break


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
for datos in data.values():
    print(datos)

test='https://www.fincaraiz.com.co/casa-en-venta/cali/prados_del_norte-det-5998080.aspx'
r =requests.get(test)
soup = BeautifulSoup(r.content,'html.parser')










# diccionario = {
#      "clave1":234,
#      "clave2":True,
#      "clave3":"Valor 1",
#      "clave4":[1,2,3,4]
#  }

# d={

#     "properties": [
#         {
#         "title": "Cali Brisas de los Alamos",
#         "price": "$ 250.000.000",
#         },{
#         "title": "Cali Brisas sur de cali",
#         "price": "$ 21231232150.000.000",
#         }
#     ]}

# print(d.items())

# print()
# print()

# print(d["properties"][0].setdefault("color ", 10))



# https://serve8.recordbate.com/tasty_hot_latinas/tasty_hot_latinas_2020-11-28_02_39.mp4?md5=KqgFdK9h9vY4ypYiJdWYow&expires=1612131348
# https://serve11.recordbate.com/tasty_hot_latinas/tasty_hot_latinas_2020-12-18_02_52.mp4?md5=QaG_5X4JSqIBftSsIdjyXQ&expires=1612131344