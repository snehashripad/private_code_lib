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


def get_gp_links(driver):
    gp_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links = [x.get_attribute('href').strip() for x in gp_links]
    return links


def ac_links(driver):
    ac_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links_ = [x.get_attribute('href').strip() for x in ac_links]
    unique_ac_links = list(dict.fromkeys(links_))
    assembly_names = []
    for link in unique_ac_links:
        assembly_name = link.split('/')[-1].replace('-', ' ').title()
        assembly_names.append(assembly_name)
        driver.get(link)
        sleep(2)
        gp_links = get_gp_links(driver)
        all_gp_data = []
        gp_names = []
        for link in gp_links[1::2]:
            gp_name = link.split('/')[-1].replace('-', ' ').title()
            gp_names.append(gp_name)
            response = requests.get(link)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.content, 'html.parser')
                gram_panchayat_name = soup.find('h1').text.strip()
                tables = pd.read_html(response.text)
                h2_tags = soup.find_all('h2', class_='display-2')
                h2_table_pairs = zip(h2_tags, tables)

                json_tables = {}

                for h2, table in h2_table_pairs:
                    # Extract the text of the h2 tag
                    heading = h2.text.strip()
                    table = table.where(pd.notnull(table), None)
                    json_obj = table.to_dict(orient='records')
                    json_tables[heading] = json_obj

                all_gp_data[gram_panchayat_name] = json_tables

            sleep(3)
        for gram_panchayat_name, gp_data in all_gp_data.items():
            write_json(gp_data, fr'D:\Tamilnadu\PC\Virudhunagar\{gram_panchayat_name}.json')

        sleep(2)
        driver.close()
        exit(0)




def PC_details():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(rf"https://localbodydata.com/parliamentary-constituencies-list-in-tamil-nadu-state-33")
    sleep(5)
    driver.maximize_window()
    pc_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')

    links = [x.get_attribute('href').strip() for x in pc_links]
    unique_links = []

    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    first_link = unique_links[35]

    driver.get(first_link)
    ac_links(driver)


if __name__ == '__main__':
    PC_details()
