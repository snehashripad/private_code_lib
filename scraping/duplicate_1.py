import os
from urllib.parse import urlparse

from srsly import write_json

import json
from time import sleep

import pandas as pd
import requests
import srsly
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

WORKING_DIR = fr'D:\Tamilnadu'
PC_name = 'Arrakonam'

clean_list = []


# def update_com_list(all_gp_data):
#     clean_list.append(all_gp_data)
#     # Use pandas to handle NaN values
#     clean_data = json.loads(pd.json.dumps(clean_list, default_handler=lambda x: None))
#     srsly.write_json(rf'D:\Tamilnadu\{PC_name}.json', clean_data)




def ac_links(driver):
    ac_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links_ = [x.get_attribute('href').strip() for x in ac_links]
    unique_links = []

    for i in links_:
        if i not in unique_links:
            unique_links.append(i)
    for _link in unique_links:
        # driver.get(_link)
        response = requests.get(_link)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table")

        if table:
            # Find the index of the column containing assembly names
            headers = table.find_all("th")
            assembly_name_column_index = None
            for i, header in enumerate(headers):
                if "assembly" in header.text.lower():
                    assembly_name_column_index = i
                    break

            if assembly_name_column_index is not None:
                # Find the assembly names from the table
                assembly_names = [row.find_all("td")[assembly_name_column_index].text.strip() for row in
                                  table.find_all("tr")[1:]]

                if assembly_names:
                    # Remove duplicates
                    unique_assembly_names = list(set(assembly_names))

                    # Change working directory
                    new_working_directory = "D:\Tamilnadu"
                    os.chdir(new_working_directory)

                    # Create folders
                    for name in unique_assembly_names:
                        folder_name = name.replace(" ", "_").lower()
                        # Match assembly names with the link provided
                        if folder_name in urlparse(_link).path:
                            if not os.path.exists(folder_name):
                                os.makedirs(folder_name)
                            print(f"Folder '{folder_name}' created in '{new_working_directory}'.")
                else:
                    print("No assembly names found in the table.")
            else:
                print("Assembly name column not found in the table.")
        else:
            print("Table not found on the page.")



        gp_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
        links = [x.get_attribute('href').strip() for x in gp_links]
        all_gp_data = []
        for link in links[1::2]:
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
                    table = table.where(pd.notnull(table), None)  # Replace NaN with None
                    json_obj = table.to_dict(orient='records')
                    json_tables[heading] = json_obj
                gp_data[gram_panchayat_name] = json_tables
                all_gp_data.append(gp_data)
        clean_data = json.loads(json.dumps(all_gp_data, default=lambda x: None))
        write_json(clean_data, folder_name)
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
    first_link = unique_links[4]

    driver.get(first_link)
    ac_links(driver)






if __name__ == '__main__':
    PC_details()
