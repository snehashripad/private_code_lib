import os
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

path = r"C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe"
_options = Options()
_options.add_argument("--window-size=1920,1080")

_options.add_experimental_option('detach', True)
service = Service(executable_path=path)


def ensure_dirs(path):
    os.makedirs(path, exist_ok=True)


def form_20():
    driver = webdriver.Chrome(service=service, options=_options)
    driver.get(rf"https://ceotelangana.nic.in/GE_2004/indexw.html")
    sleep(5)

    links = driver.find_elements(By.CSS_SELECTOR, 'table[align="center"]')
    # links = driver.find_elements(By.CSS_SELECTOR, 'table[class ="xl020192"]')

    anchor_links = links[0].find_elements(By.CSS_SELECTOR, 'a')
    pdf_links = [x.get_attribute('href').strip() for x in anchor_links]
    print(pdf_links)
    for pdf_url in pdf_links:
        try:
            response = requests.get(pdf_url, timeout=30)
            if response.status_code == 200:
                # Get the content of the response (the PDF file)
                pdf_content = response.content
                folder_path = rf"D:\form_20\Telangana\GENERAL ELECTIONS-2004\Assembly Constituencies"
                ensure_dirs(folder_path)
                # Specify the file path where you want to save the PDF
                file_name = pdf_url.split('/')[-1]
                file_path = os.path.join(folder_path, file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "wb") as pdf_file:
                        pdf_file.write(pdf_content)
                    print(f"PDF downloaded successfully: {file_name}")
                else:
                    print(f"PDF already exists: {file_name}")
            else:
                print(f"Failed to download PDF from: {pdf_url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading PDF from: {pdf_url}. Error: {e}")

        sleep(4)


if __name__ == '__main__':
    form_20()
