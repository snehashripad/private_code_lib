import srsly
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

path = r"/Drivers/chromedriver.exe"
options = Options()
# options.headless = True  # Set to true so browser window is not displayed
options.add_experimental_option('detach', True)
service = Service(executable_path=path)

com_list = []
def update_com_list(awdc_schema):
    com_list.append(awdc_schema)
    srsly.write_json(rf'C:\temp\sec_awdc.json', com_list)


def ac_scraping():
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 720)
    driver.get(r'https://hyderabad.telangana.gov.in/secunderabad-anganwadi-centers/')
    driver.maximize_window()
    sleep(3)

    rows = driver.find_elements(by=By.XPATH, value='//*[@id="post-23021"]/table/tbody/tr')
    sleep(3)
    count = len(rows)
    sleep(3)
    complete_list = []
    for i in range(1, count+1):
        dict_awc = {}
        dict_awc['sl_no'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[1]')[0].text
        dict_awc['AWC_ID'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[2]')[0].text
        dict_awc['name_of_the_mandal'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[3]')[0].text
        dict_awc['AWC_name'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[4]')[0].text
        dict_awc['AWC_type'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[5]')[0].text
        dict_awc['Sector'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[6]')[0].text
        dict_awc['AWW_name'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[7]')[0].text
        dict_awc['AWH_name'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[8]')[0].text
        dict_awc['AWW_mobile'] = driver.find_elements(by=By.XPATH, value=f'//*[@id="post-23021"]/table/tbody/tr[{i}]/td[9]')[0].text
        complete_list.append(dict_awc)
        sleep(3)

    awdc_schema = {}
    awdc_schema['secunderabad_awdc'] = complete_list
    update_com_list(awdc_schema)
# C:\temp\sec_awdc



if __name__ == '__main__':
        ac_scraping()
