import os

import json
from time import sleep
import srsly
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def write_json(obj, filepath, ensure_ascii=False):
    with open(filepath, "w", encoding="utf8", errors='ignore') as f:
        json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_ac_links(driver):
    ac_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links = [x.get_attribute('href').strip() for x in ac_elements]
    unique_links = list(dict.fromkeys(links))
    return unique_links



def read_ac_table(driver, base_directory):
    unique_links = get_ac_links(driver)
    assembly_names = []
    for link in unique_links:
        assembly_name = link.split('/')[-1].replace('-', ' ').title()
        assembly_names.append(assembly_name)
    all_ac_data = []
    for index, _link in enumerate(unique_links):
        assembly_name = assembly_names[index]

        # directory
        directory = os.path.join(base_directory, assembly_name)
        create_directory(directory)

        response = requests.get(_link)
        response.encoding = response.apparent_encoding

        tables = pd.read_html(response.text)

        if not tables:
            raise ValueError("No tables found on the page.")

        table = tables[0]
        table = table.where(pd.notnull(table), None)

        # Convert the DataFrame to a list of dictionaries
        json_obj = table.to_dict(orient='records')

        all_ac_data.append(json_obj)
        write_json(json_obj, os.path.join(directory, "data.json"))
        sleep(3)




def PC_details():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(rf"https://localbodydata.com/parliamentary-constituencies-list-in-maharashtra-state-27")
    sleep(5)
    driver.maximize_window()
    pc_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')

    links = [x.get_attribute('href').strip() for x in pc_links]
    unique_links = []
    [unique_links.append(link) for link in links if link not in unique_links]
    pc_names = []

    # first_link = unique_links[0]
    for link in unique_links:
        pc_link = link.split('/')[-1].replace('-', ' ').title()
        pc_names.append(pc_link)
        base_directory = fr'D:\GP_details\{pc_link}'
        create_directory(base_directory)
        sleep(2)

        driver.get(link)
        sleep(2)
        get_ac_links(driver, base_directory)
        sleep(2)
    driver.quit()


if __name__ == '__main__':
    PC_details()