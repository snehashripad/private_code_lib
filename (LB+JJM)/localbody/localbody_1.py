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
    try:
        with open(filepath, "w", encoding="utf8", errors='ignore') as f:
            json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)
        print(f"Successfully wrote JSON to {filepath}")
    except Exception as e:
        print(f"Error writing JSON to {filepath}: {e}")


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_pc_links(driver):
    driver.get(rf"https://localbodydata.com/parliamentary-constituencies-list-in-maharashtra-state-27")
    sleep(5)
    pc_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links = [x.get_attribute('href').strip() for x in pc_links]
    unique_links = list(dict.fromkeys(links))  # Removes duplicates while preserving order
    return unique_links

def process_pc(driver, pc_links):
    for _ in pc_links:
        first_link = pc_links[4]
        pc_name = first_link.split('/')[-1].replace('-', ' ').title()
        base_directory = rf'D:\Maharastra\pc\{pc_name}'
        create_directory(base_directory)
        sleep(1)
        ac_links = get_ac_links(driver)
        for ac_link in ac_links:
            ac_name = ac_link.split('/')[-1].replace('-', ' ').title()
            ac_directory = os.path.join(base_directory, ac_name)
            create_directory(ac_directory)
            sleep(1)

            driver.get(ac_link)
            sleep(2)
            read_gp_tables(driver, ac_directory, ac_name)


def get_ac_links(driver):
    ac_elements = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links = [x.get_attribute('href').strip() for x in ac_elements]
    unique_links = list(dict.fromkeys(links))
    return unique_links


def get_gp_link(driver):
    gp_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links = [x.get_attribute('href').strip() for x in gp_links]
    # unique_gp_links = list(dict.fromkeys(links))
    return links


def read_gp_tables(driver, ac_directory, ac_name):

    unique_gp_links = get_gp_link(driver)
    all_gp_data = {}
    for link in unique_gp_links[1::2]:
        response = requests.get(link)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content, 'html.parser')
            gram_panchayat_name = soup.find('h1').text.strip()
            tables = pd.read_html(response.text)
            h2_tags = soup.find_all('h2', class_='display-2')
            h2_table_pairs = zip(h2_tags, tables)
            gp_data = {}
            json_tables = {}

            for h2, table in h2_table_pairs:
                # Extract the text of the h2 tag
                heading = h2.text.strip()
                table = table.where(pd.notnull(table), None)
                json_obj = table.to_dict(orient='records')
                json_tables[heading] = json_obj
            all_gp_data[gram_panchayat_name] = json_tables
    #construct the file path
    write_json(all_gp_data, os.path.join(ac_directory, "data.json"))
    sleep(1)



def setup_driver():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver


def pc_details():
    driver = setup_driver()
    try:
        pc_links = get_pc_links(driver)
        process_pc(driver, pc_links)
    finally:
        driver.quit()


if __name__ == '__main__':
    pc_details()
