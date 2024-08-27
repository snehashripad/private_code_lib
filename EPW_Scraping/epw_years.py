# import glob
# import random
#
# from pandas.io.common import file_exists
# from selenium import webdriver
# import time
# import os
# import json
# import requests
# import urllib3
#
#
# from selenium.webdriver import ActionChains
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# def get_year_(driver):
#     # year_list = []
#
#     year_links = driver.find_elements(By.CSS_SELECTOR, "span[class='fieldset-legend']")[0:]
#     # year = year_links[0].text.split('\n')[1]
#
#     # create_new_folder()
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='fieldset-legend']")))
#
#     with open(fr'C:\Users\HP\PycharmProjects\python_selenium_project\EPW_Scraping\sample.txt', 'w') as f:
#         year_list = []
#         for index, item in enumerate(year_links):
#             year = item.text.split('\n')[1]
#             print(index, year)
#             year_list.append(year)
#         f.write(f'{year_list}\n')
#
#         # year_list.append(year)
#     print(year_list)
#
#
# def kill_all_open_chrome_instances():
#     os.system('taskkill /f /fi "imagename eq chrome*')
#
#
# if __name__ == '__main__':
#     # download_pdf(f"https://www.epw.in/system/files/pdf/2023_58/45-46/ED_LVIII_45-46_181123_A%2070-hour%20Workweek.pdf",rf"D:\pdf\002.pdf")
#
#     kill_all_open_chrome_instances()
#     options = webdriver.ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-notifications")
#     options.add_argument("--start-maximized")
#     options.add_argument(rf"--user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data")
#     options.add_argument(f"--profile-directory=Profile 4")
#
#     urllib3.disable_warnings()
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     # driver = webdriver.Chrome(options=options)
#     driver.get(f'https://www.epw.in/journal/epw-archive')
#     driver.implicitly_wait(2)
#     get_year_(driver)
