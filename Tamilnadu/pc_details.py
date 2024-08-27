import requests
from bs4 import BeautifulSoup
import time

# URL of the webpage
url = "https://localbodydata.com/gram-panchayats-list-in-assembly-arcot-3858"

# Fetch the webpage content
response = requests.get(url)
webpage_content = response.text

# Parse the webpage content
soup = BeautifulSoup(webpage_content, "html.parser")

# Find the table containing the Gram Panchayat data
table = soup.find("table")

# Extract the base URL for relative links
base_url = "https://localbodydata.com/"

# Loop through the table rows and extract data
for row in table.find_all("tr")[1:]:  # Skip the header row
    cells = row.find_all("td")
    gram_panchayat_link = cells[0].find("a")
    gram_panchayat_name = gram_panchayat_link.text.strip()
    gram_panchayat_url = base_url + gram_panchayat_link["href"]

    # Fetch the Gram Panchayat page
    gram_panchayat_response = requests.get(gram_panchayat_url)
    gram_panchayat_content = gram_panchayat_response.text
    gram_panchayat_soup = BeautifulSoup(gram_panchayat_content, "html.parser")

    # Extract the assembly name from the Gram Panchayat page
    # Assuming the assembly name is in a specific tag (update selector based on actual HTML)
    assembly_name_tag = gram_panchayat_soup.find("tag_containing_assembly_name")
    if assembly_name_tag:
        assembly_name = assembly_name_tag.text.strip()
    else:
        assembly_name = "Assembly name not found"

    print(f"Gram Panchayat: {gram_panchayat_name}, Assembly: {assembly_name}, Link: {gram_panchayat_url}")

    # Wait before making the next request to avoid overwhelming the server
    time.sleep(1)

# from time import sleep
# import srsly
# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.support.ui import WebDriverWait
#
# clean_list = []
#
#
# def update_com_list(gp_schema):
#     clean_list.append(gp_schema)
#     srsly.write_json(rf'D:\Tamilnadu\pallur.json', clean_list)
#
#
# def gp_mem(driver):
#     gp_table_rows = driver.find_elements(By.XPATH, '/html/body/div[3]/div[9]/div/div/table/tbody/tr')
#     count = len(gp_table_rows)
#     sleep(1)
#     list_gp_mems = []
#
#     for i in range(1, count + 1):
#         dict_gp_mem = {}
#         dict_gp_mem['sl.no'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[9]/div/div/table/tbody/tr[{i}]/td[1]')[0].text
#         dict_gp_mem['member_name'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[9]/div/div/table/tbody/tr[{i}]/td[2]')[0].text
#         dict_gp_mem['Designation'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[9]/div/div/table/tbody/tr[{i}]/td[3]')[0].text
#         dict_gp_mem['mobile_no'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[9]/div/div/table/tbody/tr[{i}]/td[4]')[0].text
#         dict_gp_mem['email'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[9]/div/div/table/tbody/tr[{i}]/td[5]')[0].text
#         list_gp_mems.append(dict_gp_mem)
#     return list_gp_mems
#
# def gp_schools(driver):
#     # schools = driver.find_elements(By.XPATH, '/html/body/div[3]/div[9]/div/div/table')[0].text
#     sleep(1)
#     gp_table_school_rows = driver.find_elements(By.XPATH, '/html/body/div[3]/div[10]/div/div/table/tbody/tr')
#     count = len(gp_table_school_rows)
#     sleep(1)
#     list_schools = []
#     for i in range(1, count + 1):
#         dict_gp_school = {}
#         dict_gp_school['no'] = \
#         driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[1]')[0].text
#         dict_gp_school['name'] = \
#         driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[2]')[0].text
#         dict_gp_school['Management'] = \
#         driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[3]')[0].text
#         dict_gp_school['Category'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[4]')[0].text
#         dict_gp_school['Boys'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[5]')[0].text
#         dict_gp_school['Girls'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[6]')[0].text
#         dict_gp_school['Teachers'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[7]')[0].text
#         dict_gp_school['School_code'] = \
#             driver.find_elements(By.XPATH, f'/html/body/div[3]/div[10]/div/div/table/tbody/tr[{i}]/td[8]')[0].text
#         list_schools.append(dict_gp_school)
#     return list_schools
#
#
# def gp_wards(driver):



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


def ac_links(driver):
    ac_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links_ = [x.get_attribute('href').strip() for x in ac_links]
    unique_links = []
    all_ac_data = []
    assembly_names = []
    for link in links_:
        if link not in unique_links:
            unique_links.append(link)
            # Extract the Assembly Constituency name from the link text
            assembly_name = link.split('/')[-1].replace('-', ' ').title()
            assembly_names.append(assembly_name)
    # Iterate through each unique link
    all_ac_data = []
    for index, _link in enumerate(unique_links):
        assembly_name = assembly_names[index]

        # Create a directory for the Assembly Name
        directory = f"D:\GP_details/{assembly_name}.json"
        create_directory(directory)

        response = requests.get(_link)
        response.encoding = response.apparent_encoding

        # Use pandas to read the HTML tables
        tables = pd.read_html(response.text)

        if not tables:
            raise ValueError("No tables found on the page.")

        # Assuming the first table is the desired one
        table = tables[0]
        table = table.where(pd.notnull(table), None)  # Replace NaN with None for JSON compatibility

    # Convert the DataFrame to a list of dictionaries
        json_obj = table.to_dict(orient='records')

        all_ac_data.append(json_obj)
        write_json(all_ac_data, directory)
        sleep(2)
        driver.close()
exit(0)


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

    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    first_link = unique_links[0]

    driver.get(first_link)
    ac_links(driver)


if __name__ == '__main__':
    PC_details()

#
#     gp_table_ward_rows = driver.find_elements(By.XPATH, '/html/body/div[3]/div[8]/div/div/table/tbody/tr')
#
#     count = len(gp_table_ward_rows)
#     sleep(1)
#     list_ward = []
#     for i in range(1, count + 1):
#         dict_ward = {}
#         dict_ward['no'] = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[8]/div/div/table/tbody/tr[{i}]/td[1]')[0].text
#         dict_ward['ward_name'] = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[8]/div/div/table/tbody/tr[{i}]/td[2]')[0].text
#         dict_ward['ward_no'] = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[8]/div/div/table/tbody/tr[{i}]/td[3]')[0].text
#         dict_ward['LGD_code'] = \
#         driver.find_elements(By.XPATH, f'/html/body/div[3]/div[8]/div/div/table/tbody/tr[{i}]/td[4]')[0].text
#         list_ward.append(dict_ward)
#     return list_ward
#
#
#
# def gp_links(driver):
#     gp_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
#     links = [x.get_attribute('href').strip() for x in gp_links]
#     all_gp_data = {}
#     for link in links[1::2]:
#         # r_link = links[62]
#         driver.get(links[133])
#         sleep(3)
#         ward = gp_wards(driver)
#         mem_xpath = driver.find_elements(By.XPATH, '/html/body/div[3]/div[9]/div/h2')[0].text
#         if mem_xpath == 'Members':
#             members = gp_mem(driver)
#         else:
#             members = []
#         school_xpath = driver.find_elements(By.CSS_SELECTOR, '/html/body/div[3]/div[10]/div/h2')[0].text
#         if school_xpath == 'Schools':
#             schools = gp_schools(driver)
#         else:
#             schools = []
#         all_gp_data[link]={
#             'ward': ward,
#             'members' : members,
#             'schools': schools
#         }
#     return all_gp_data
#
#
# def PC_details():
#     options = FirefoxOptions()
#     # options.add_argument("--headless")
#     driver = webdriver.Firefox(options=options)
#     driver.get(rf"https://localbodydata.com/parliamentary-constituencies-list-in-tamil-nadu-state-33")
#     sleep(5)
#     driver.maximize_window()
#     pc_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
#
#     links = [x.get_attribute('href').strip() for x in pc_links]
#     # links = set(links)
#     unique_links = []
#
#     for link in links:
#         if link not in unique_links:
#             unique_links.append(link)
#     first_link = unique_links[0]
#
# # for link in unique_links:
#     driver.get(first_link)
#
#     ac_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
#     links_ = [x.get_attribute('href').strip() for x in ac_links]
#     # links_ = set(links_)
#     for link in links_:
#         driver.get(link)
#         sleep(2)
#
#         table_rows = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr')
#         count = len(table_rows)
#         sleep(1)
#         complete_list = []
#         for i in range(1, count + 1):
#             dict_village_details = {}
#             dict_village_details['Sl.no'] = \
#                 driver.find_elements(By.XPATH,
#                                      f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[1]')[
#                     0].text
#             dict_village_details[' Village_name'] = driver.find_elements(By.XPATH,
#                                                                          f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[2]')[
#                 0].text
#             dict_village_details['Gram_panchayat_name'] = driver.find_elements(By.XPATH,
#                                                                                f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[3]')[
#                 0].text
#             dict_village_details['Sub_dristrict_name'] = driver.find_elements(By.XPATH,
#                                                                               f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[4]')[
#                 0].text
#             dict_village_details['District_name'] = driver.find_elements(By.XPATH,
#                                                                          f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[5]')[
#                 0].text
#             dict_village_details['AC_name'] = driver.find_elements(By.XPATH,
#                                                                    f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[6]')[
#                 0].text
#             dict_village_details['PC_name'] = driver.find_elements(By.XPATH,
#                                                                    f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[7]')[
#                 0].text
#
#             complete_list.append(dict_village_details)
#             gp_schema = {'GP_details': dict_village_details, 'gp_mem' : gp_links(driver)}
#             update_com_list(gp_schema)
#
#
# if __name__ == '__main__':
#     PC_details()
