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
def update_com_list(rangareddy_dist_schema):
    com_list.append(rangareddy_dist_schema)
    srsly.write_json(rf'C:\temp\ngos.json', com_list)

def ngos_scraping():
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 720)
    driver.get(r'https://rangareddy.telangana.gov.in/public-utility-category/ngos/')
    driver.maximize_window()
    sleep(3)
    # item.text.split('\n')
    div_class = driver.find_elements(by=By.XPATH, value='//*[@id="row-content"]/div/div/div')
    sleep(3)
    ngos_list = []
    for item in div_class:
        # ngos_list.append(item)
        dict_ngos = {}
        dict_ngos['org_name'] = item.text.split('\n')[0]
        dict_ngos['org_address'] = item.text.split('\n')[1]
        dict_ngos['org_email'] = item.text.split('\n')[2]
        dict_ngos['ph_no'] = item.text.split('\n')[3]
        dict_ngos['website_link'] = item.text.split('\n')[4]
        dict_ngos['category/type'] = item.text.split('\n')[5]
        dict_ngos['pincoe'] = item.text.split('\n')[6]
        ngos_list.append(dict_ngos)
        sleep(3)

    rangareddy_dist_schema = {}
    rangareddy_dist_schema['rangareddy_dist_ngo'] = ngos_list
    update_com_list(rangareddy_dist_schema)


if __name__ == '__main__':
        ngos_scraping()
