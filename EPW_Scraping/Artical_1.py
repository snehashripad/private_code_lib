from selenium import webdriver
import time
import os
import json
import requests

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup



def get_all_links(driver):
    article_links = driver.find_elements(By.CSS_SELECTOR, '.block-inner .views-field-title a')

    links = [x.get_attribute('href').strip() for x in article_links]
    # links = set(links)

    for index, href in enumerate(links):
        if href == 'https://www.epw.in/book-store':
            links.remove(href)
        else:
            driver.get(href)
            try:
                download_pdf = \
                    driver.find_elements(by=By.XPATH,
                                         value=f'//*[@id="block-block-144--2"]/div/div/div/div/div/span/a')[0]
                link_ = download_pdf.get_attribute('href')

            except:
                download_pdf = driver.find_elements(by=By.XPATH, value=f'//a[contains(text(),"Download PDF")]')[0]
                link_ = download_pdf.get_attribute('href')
            if download_pdf.get_attribute('href') and '.pdf' in download_pdf.get_attribute('href') and 'dowload' in download_pdf.text.lower:
                download_pdf.click()
                print(link_)






            # get_pdf_link(driver)
            time.sleep(3)





def kill_all_open_chrome_instances():
    os.system('taskkill /f /fi "imagename eq chrome*')


if __name__ == '__main__':
    kill_all_open_chrome_instances()
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument(rf"--user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data")
    options.add_argument(f"--profile-directory=Profile 3")
    options.add_experimental_option('prefs', {"download.default_directory": "C:\temp\data",
                                              "download.prompt_for_download": False,
                                              "plugin.always_open_pdf_externally": True})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(options=options)

    for year in range(2023, 2024):
        for click in range(1, 201):
            driver.get(rf"https://www.epw.in/journal/{year}/{click}")

            article_links = driver.find_elements(By.CSS_SELECTOR, '.block-inner .views-field-title a')

            links = [x.get_attribute('href').strip() for x in article_links]
            # links = set(links)

            for index, href in enumerate(links):
                if href == 'https://www.epw.in/book-store':
                    links.remove(href)
                else:
                    driver.get(href)
                    try:
                        download_pdf = \
                            driver.find_elements(by=By.XPATH,
                                                 value=f'//*[@id="block-block-144--2"]/div/div/div/div/div/span/a')[0]
                        link_ = download_pdf.get_attribute('href')

                    except:
                        download_pdf = driver.find_elements(by=By.XPATH, value=f'//a[contains(text(),"Download PDF")]')[
                            0]
                        link_ = download_pdf.get_attribute('href')
                    if download_pdf.get_attribute('href') and '.pdf' in download_pdf.get_attribute(
                            'href') and 'download' in download_pdf.text.lower():
                        download_pdf.click()
                        print(link_)


            # time.sleep(3)
            #
            # get_all_links(driver)