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
import logging


def setup_logging():
    logging.basicConfig(
        filename='scraper.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )


def write_json(obj, filepath, ensure_ascii=False):
    try:
        with open(filepath, "w", encoding="utf8", errors='ignore') as f:
            json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)
        logging.info(f"Successfully wrote JSON to {filepath}")
    except Exception as e:
        logging.error(f"Error writing JSON to {filepath}: {e}")


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory {directory}")


def get_pc_links(driver):
    driver.get(rf"https://localbodydata.com/parliamentary-constituencies-list-in-madhya-pradesh-state-23")
    sleep(5)
    pc_links = driver.find_elements(By.XPATH, '*//tbody//a')
    links = [x.get_attribute('href').strip() for x in pc_links]
    unique_links = list(dict.fromkeys(links))  # Removes duplicates while preserving order
    return unique_links


def process_pc(driver, pc_links):
    for link in pc_links:
        pc_name = link.split('/')[-1].replace('-', ' ').title()
        base_directory = rf'D:\GP_details\Madhya Pradesh\PC\{pc_name}'
        create_directory(base_directory)
        sleep(2)

        driver.get(link)
        sleep(2)
        ac_links = get_ac_links(driver)
        for ac_link in ac_links:
            ac_name = ac_link.split('/')[-1].replace('-', ' ').title()
            ac_directory = os.path.join(base_directory, ac_name)
            create_directory(ac_directory)
            sleep(1)

            driver.get(ac_link)
            sleep(2)
            read_gp_tables(driver, ac_directory)


def get_ac_links(driver):
    ac_elements = driver.find_elements(By.XPATH, '*//tbody//a')
    links = [x.get_attribute('href').strip() for x in ac_elements]
    unique_links = list(dict.fromkeys(links))
    return unique_links


def get_gp_links(driver):
    gp_links = driver.find_elements(By.XPATH, '*//tbody//a')
    links = [x.get_attribute('href').strip() for x in gp_links]
    return links


def fetch_html_content(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return BeautifulSoup(response.content, 'html.parser')
        else:
            logging.error(f"Error fetching content from {link}: Status code {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Exception fetching content from {link}: {e}")
        return None


def parse_gp_data(soup):
    gp_data = {}
    h1_tag = soup.find('h1')
    if h1_tag:
        gram_panchayat_name = h1_tag.text.strip()
    else:
        logging.warning("No <h1> tag found.")
        return None

    try:
        tables = pd.read_html(str(soup))
        h2_tags = soup.find_all('h2', class_='display-2')
        h2_table_pairs = zip(h2_tags, tables)
        json_tables = {}

        for h2, table in h2_table_pairs:
            heading = h2.text.strip()
            table = table.where(pd.notnull(table), None)
            json_obj = table.to_dict(orient='records')
            json_tables[heading] = json_obj

        gp_data[gram_panchayat_name] = json_tables
    except ValueError as ve:
        logging.error(f"No tables found: {ve}")
    except Exception as e:
        logging.error(f"Error parsing GP data: {e}")

    return gp_data


def save_gp_data(ac_directory, gp_data):
    if gp_data:
        write_json(gp_data, os.path.join(ac_directory, "data.json"))
    else:
        logging.warning("No data to save.")


def read_gp_tables(driver, ac_directory):
    unique_gp_links = get_gp_links(driver)
    all_gp_data = {}
    for link in unique_gp_links[1::2]:  # skipping every other link as in original code
        if 'null-null' in link:
            logging.warning(f"Skipping link due to 'null-null' in URL: {link}")
            continue

        soup = fetch_html_content(link)
        if soup:
            gp_data = parse_gp_data(soup)
            if gp_data:
                all_gp_data.update(gp_data)
        else:
            logging.error(f"Skipping link due to repeated errors: {link}")
    save_gp_data(ac_directory, all_gp_data)
    sleep(1)


def setup_driver():
    options = FirefoxOptions()
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
    setup_logging()
    pc_details()
