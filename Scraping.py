from bs4 import BeautifulSoup 
import requests
import json 
import re

zones=['norte','sur','oeste','oriente',]
baseurl ='https://www.fincaraiz.com.co/casas/venta/{}/cali/'.format(zones[0])
page =requests.get(baseurl)
soup=BeautifulSoup(page.content, 'html.parser')


urls=soup.find_all('div',class_='span-title')
# print("numero de inmuebles", len(urls))

urllist=[]
comoseria =[]
nuevo=[]

for i in urls:
    for x in i.find_all('a',href=True):
        comoseria.append(x['href'])
        
# print(len(comoseria))

aux=0
for hola in comoseria:
    if hola.startswith("https") ==False:
        nuevo.append('https://www.fincaraiz.com.co{}'.format(hola))
        aux+=1
        
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(nuevo, f, ensure_ascii=False, indent=4)

# print(aux)

testurl='https://www.fincaraiz.com.co/casa-en-venta/cali/los_andes-det-5712022.aspx'
r =requests.get(testurl)
soup = BeautifulSoup(r.content,'html.parser')
aja=soup.find('div' , class_='price')

# body=[tag for tag in aja if 'h2'][1]
# print(body)

# ala=0
# for datos in nuevo:
#     r =requests.get(datos)
#     soup = BeautifulSoup(r.content,'html.parser')
#     peo=soup.find('div' , class_='price')
#     ala+=1
#     print(ala,"prices : {}".format((peo.text).strip()))





# repr(string) imprimir los espacios 
# tittle=soup.find('span', {'style':'font-weight:normal'})

# print(tittle.text)

# for divs in tittle:
#     finddivs=divs.find('span')
#     print(finddivs)




# mts=soup.find('span',{'class':'advertSurface'})
# rooms=soup.find('span',{'class':'advertRooms'})
# baths=soup.find('span',{'class':'advertBaths'})
# parking=soup.find('span',{'class':'advertGarages'})


# mts=mts.text
# rooms=rooms.text
# baths=baths.text
# parking=parking.text


# xx=rooms.split(':')
# xxx=baths.split(':')
# xxxx=parking.split(':')


# print(repr(xx[1].strip()))
# print(repr(xxx[1].strip()))
# print(repr(xxxx[1].strip()))

whatsap=soup.find('div',{'class':'a_options whatsapplink'}).get('onclick')


line =str(whatsap)
# getwhats=line.replace("'","").replace(";","").replace(")","")

haaaa=line.split(",")
print(haaaa[1].replace("'","").replace(")","").replace(";",""))


print(type(haaaa[1]))