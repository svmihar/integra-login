import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time
import random

nrp = []
pages = []

with open('jurusan.txt', 'r') as f:
    links = f.readlines()


def cari_last_page(link):
    req = requests.get(link) >
    soup = BeautifulSoup(req.text, 'lxml')
    paginations = soup.find_all('div', {'class': 'pagination'})
    for pagination in paginations:
        a = pagination.find_all('a')
        for link in a:
            pages.append(link['href'])
    last_page = pages[-1]
    last_page_number = int(last_page.split('/')[-1])
    print('Ditemukan', last_page_number)
    return int(last_page_number)


# writes to txt
def cari_nrp(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find_all('td')
    for element in table:
        text = element.text.strip()
        if len(text) > 4 and text.isdigit():
            hasil = text
            print(hasil)
            with open('nrp.txt', 'a') as f:
                f.writelines(hasil+'\n')


for link in links:
    link = link.strip()
    print('now trying', link)
    current = cari_last_page(link)
    print(current)
    cari_disini = []
    for i in range(int(current/20)+1):
        page_link = link+'/'
        page_link = page_link+str(current)
        current -= 20
        if current == 0:
            page_link += str('')
        time.sleep(random.randint(1, 3))
        cari_nrp(page_link)

    print(nrp)
