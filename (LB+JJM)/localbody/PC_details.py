from time import sleep
import srsly
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

clean_list = []


def update_com_list(gp_schema):
    clean_list.append(gp_schema)
    srsly.write_json(rf'D:\GP_details\Pallur.json', clean_list)


def PC_details():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(rf"https://localbodydata.com/parliamentary-constituencies-list-in-maharashtra-state-27")
    sleep(5)
    driver.maximize_window()
    pc_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')

    links = [x.get_attribute('href').strip() for x in pc_links]
    # links = set(links)
    unique_links = []

    for link in links:
        if link not in unique_links:
            unique_links.append(link)


    driver.get(unique_links[1])

    ac_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links_ = [x.get_attribute('href').strip() for x in ac_links]

    unique_links2 = []

    for link in links_:
        if link not in unique_links2:
            unique_links.append(link)
    dict_village_details = {}
    # links_ = set(links_)
    for _link in unique_links2:
        driver.get(_link)
        sleep(2)
        dict_village_details = {}
        table_rows = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr')
        count = len(table_rows)
        sleep(1)
        complete_list = []
        for i in range(1, count + 1):
            dict_village_details = {}
            dict_village_details['Sl.no'] = \
                driver.find_elements(By.XPATH,
                                     f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[1]')[
                    0].text
            dict_village_details[' Village_name'] = driver.find_elements(By.XPATH,
                                                                         f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[2]')[
                0].text
            dict_village_details['Gram_panchayat_name'] = driver.find_elements(By.XPATH,
                                                                               f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[3]')[
                0].text
            dict_village_details['Sub_dristrict_name'] = driver.find_elements(By.XPATH,
                                                                              f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[4]')[
                0].text
            dict_village_details['District_name'] = driver.find_elements(By.XPATH,
                                                                         f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[5]')[
                0].text
            dict_village_details['AC_name'] = driver.find_elements(By.XPATH,
                                                                   f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[6]')[
                0].text
            dict_village_details['PC_name'] = driver.find_elements(By.XPATH,
                                                                   f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[7]')[
                0].text
            # complete_list.append(dict_village_details)
    gp_schema = {'GP_details': dict_village_details}
    update_com_list(gp_schema)


if __name__ == '__main__':
    PC_details()
