#!/usr/bin/env python

import requests
from fire import Fire
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from multiprocessing import Pool


def cari_last_page(link):
    pages = []
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    paginations = soup.find_all('div', {'class': 'pagination'})
    for pagination in paginations:
        a = pagination.find_all('a')
        for link in a:
            pages.append(link['href'])
    last_page = pages[-1]
    last_page_number = int(last_page.split('/')[-1])
    return int(last_page_number)


def cari_nrp(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find_all('td')
    return [element.text.strip() for element in table if len(element.text.strip()) > 4 and element.text.strip().isdigit()]


def pembagi(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def generate_links(list_of_links):
    hasil = []
    print('generating links...')
    for link in tqdm(list_of_links):
        c_p = cari_last_page(link)
        for _ in range(c_p):
            page = f'{link}/{c_p}'
            c_p -= 20
            hasil.append(page)
            if c_p == 0:
                hasil.append(link)
                break

    with open('link_mahasiswa.txt', 'a+') as f:
        for h in hasil:
            f.writelines(h+'\n')
    return hasil

import os
def main(n_jobs=10, chunks=100):
    links = open('jurusan.txt').read().splitlines()


    if os.path.exists('link_mahasiswa.txt'):
        print('file ditemukan')
        mahasiswa = open('link_mahasiswa.txt').read().splitlines()
        mahasiswa=list(set(mahasiswa))
    else:
        mahasiswa = generate_links(links)

    mahasiswa = list(pembagi(mahasiswa,chunks))

    for i, m in enumerate(mahasiswa):
        print(f'progress: {i}/{len(mahasiswa)}')
        with Pool(n_jobs) as p:
            hasil = list(tqdm(p.imap(cari_nrp, m), total=len(mahasiswa)))
        p.terminate()
        p.join()
        hasil_ = [x for l in hasil for x in l]
        hasil_ = list(set(hasil_))
        with open('nrp.txt', 'a+') as f:
            for h in hasil_:
                f.writelines(h+'\n')


if __name__ == '__main__':
    Fire()
