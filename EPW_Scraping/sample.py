import asyncio
import glob
import random

from pandas.io.common import file_exists
from selenium import webdriver
import time
import os
import json
import requests
import urllib3

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from EPW_Scraping.decorators import await_time_limit


def write_json(obj, filepath, ensure_ascii=False):
    with open(filepath, "w", encoding="utf8", errors='ignore') as f:
        json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)


clean_list = []


def update_clean_list(article_schema):
    clean_list.append(article_schema)
    write_json(clean_list, rf'C:\temp\Article_2018_1.json')


def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def create_new_folder(article_shcema):
    get_all_links(driver)
    folder_path = rf"D:\data\{article_shcema['year']}"
    ensure_dir(folder_path)
    print(folder_path)
    return folder_path



def get_all_links(driver):
    article_links = driver.find_elements(By.CSS_SELECTOR, '.block-inner .views-field-title a')

    links = [x.get_attribute('href').strip() for x in article_links]
    # links = set(links)

    for index, href in enumerate(links):
        if href == 'https://www.epw.in/book-store':
            links.remove(href)
        else:
            driver.get(href)
            print(index, href)
            article_schema = {'Article_link': href}

            try:
                article_schema['year'] = get_year_(driver)
            except:
                num = random.random()
                article_schema['year'] = num
            # create_new_folder()



            print(article_schema)
            return article_schema
            # update_clean_list(article_schema)
    driver.back()



def get_year_(driver):
    year_links = driver.find_elements(By.CSS_SELECTOR, "span[class='fieldset-legend']")[5:6]
    year = year_links[0].text.split('\n')[1]

    # create_new_folder()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='fieldset-legend']")))

    for index, item in enumerate(year_links):
        print(index, item.text)
        actions = ActionChains(driver)
        actions.move_to_element(item).click().perform()
        driver.implicitly_wait(5)
        list = driver.find_elements(By.CSS_SELECTOR, "div[class='fieldset-wrapper']")[5:]
        vol_links = list[0].find_elements(By.CSS_SELECTOR, "a")
        links = [x.get_attribute('href').strip() for x in vol_links][0:]
        for index, item in enumerate(links):
            print(item)

            driver.get(item)
            get_all_links(driver)
            driver.back()
    return year

# fr"D:\data.pdf"


def kill_all_open_chrome_instances():
    os.system('taskkill /f /fi "imagename eq chrome*')


if __name__ == '__main__':

    # download_pdf(f"https://www.epw.in/system/files/pdf/2023_58/45-46/ED_LVIII_45-46_181123_A%2070-hour%20Workweek.pdf",rf"D:\pdf\002.pdf")

    kill_all_open_chrome_instances()
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument(rf"--user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data")
    options.add_argument(f"--profile-directory=Profile 4")


    # folder_name = create_new_folder()
    options.add_experimental_option('prefs', {"download.default_directory": fr"D:\data.pdf",
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "plugin.always_open_pdf_externally": True})

    urllib3.disable_warnings()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.epw.in/journal/epw-archive')
    driver.implicitly_wait(2)
    get_year_(driver)

def get_year_(driver):
    year_links = driver.find_elements(By.CSS_SELECTOR, "span[class='fieldset-legend']")[5:6]
    year = year_links[0].text.split('\n')[1]


    f = create_new_folder()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='fieldset-legend']")))

    for index, item in enumerate(year_links):
        print(index, item.text)
        actions = ActionChains(driver)
        actions.move_to_element(item).click().perform()
        driver.implicitly_wait(5)
        list = driver.find_elements(By.CSS_SELECTOR, "div[class='fieldset-wrapper']")[5:]
        vol_links = list[0].find_elements(By.CSS_SELECTOR, "a")
        links = [x.get_attribute('href').strip() for x in vol_links][0:]
        for index, item in enumerate(links):
            print(item)

            driver.get(item)
            get_all_links(driver)
            driver.back()
    return year

# fr"D:\data.pdf"


def kill_all_open_chrome_instances():
    os.system('taskkill /f /fi "imagename eq chrome*')


if __name__ == '__main__':

    # download_pdf(f"https://www.epw.in/system/files/pdf/2023_58/45-46/ED_LVIII_45-46_181123_A%2070-hour%20Workweek.pdf",rf"D:\pdf\002.pdf")

    kill_all_open_chrome_instances()
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument(rf"--user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data")
    options.add_argument(f"--profile-directory=Profile 4")


    folder_name = create_new_folder()
    options.add_experimental_option('prefs', {"download.default_directory": folder_name,
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "plugin.always_open_pdf_externally": True})

    urllib3.disable_warnings()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.epw.in/journal/epw-archive')
    driver.implicitly_wait(2)
    get_year_(driver)


# def get_year_(driver):
#     year_links = driver.find_elements(By.CSS_SELECTOR, "span[class='fieldset-legend']")[5:6]
#     year = year_links[0].text.split('\n')[1]
#
#     # create_new_folder()
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='fieldset-legend']")))
#
#
#
#     for index, item in enumerate(year_links):
#         print(index, item.text)
#         actions = ActionChains(driver)
#         actions.move_to_element(item).click().perform()
#         driver.implicitly_wait(5)
#         list = driver.find_elements(By.CSS_SELECTOR, "div[class='fieldset-wrapper']")[5:]
#         vol_links = list[0].find_elements(By.CSS_SELECTOR, "a")
#         links = [x.get_attribute('href').strip() for x in vol_links][0:]
#         for index, item in enumerate(links):
#             print(item)
#
#             driver.get(item)
#             get_all_links(driver)
#             driver.back()
#     return year



        # for link in vol_links:
        #     time.sleep(5)
        #     link.click()
        #     get_all_links(driver)
        #     driver.back()
        # driver.back()

        # get_all_links(driver)

        # get_all_links(driver)
# for year in range(2023, 2024):
#     for click in range(1, 201):
#         driver.get(rf"https://www.epw.in/journal/{year}/{click}")
#         get_all_links(driver)
