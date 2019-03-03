import requests
from bs4 import BeautifulSoup
from pprint import pprint


links = 'https://forlap.ristekdikti.go.id/mahasiswa/detailsemester/RDAyNjFBNjEtMzg1RC00RTFGLTk3RjUtMDVFOEREODU1NzE2/20181'
req = requests.get(links)
soup = BeautifulSoup(req.text, 'lxml')
paginations =soup.find_all('div',{'class':'pagination'})
pages = []
for pagination in paginations: 
    a = pagination.find_all('a')
    for link in a: 
        pages.append(link['href'])
last_page = pages[-1]
last_page_number = int(last_page.split('/')[-1])

current = last_page_number
cari_disini = []
for i in range(int(last_page_number/20)+1):
    page_link = links+'/'
    page_link = page_link+str(current)
    current-=20
    if current == 0: 
        page_link+=str('')
    cari_disini.append(page_link)

for link in cari_disini: 
    last_page = requests.get(link)
    soup = BeautifulSoup(last_page.text, 'lxml')
    table = soup.find_all('td')

    nrp = []
    for element in table: 
        nrp.append(element.text.strip())
    nrp.sort()
    nrp = nrp[0:20]
    print(nrp)
    for nrp in nrp: 
        with open('nrp.txt','a') as f: 
            f.writelines(nrp+'\n')


""" last_page = requests.get(last_page) 

soup = BeautifulSoup(last_page.text, 'lxml')
table = soup.find_all('td')

nrp = []
for element in table: 
    nrp.append(element.text.strip())
nrp.sort()
nrp = nrp[0:20]
print(nrp) """