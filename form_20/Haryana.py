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
    driver.get(rf"https://ceoharyana.gov.in/WebCMS/Start/1449")
    sleep(5)
    election_type = driver.find_elements(By.XPATH, '//*[@id="ElectionType"]')[0].text.split('\n')[3:4]
    for type in election_type:
        type = type.strip()
        driver.find_elements(By.XPATH, f'//*[@id="ElectionType"]/option[text()="{type}"]')[0].click()
        sleep(3)
        election_year = driver.find_elements(By.XPATH, '//*[@id="YearId"]')[0].text.split('\n')[4:5]
        for year in election_year:
            year = year.strip()
            driver.find_elements(By.XPATH, f'//*[@id="YearId"]/option[text()="{year}"]')[0].click()
            sleep(4)
            driver.find_elements(By.XPATH, '//*[@id="content_location_1"]/div[2]/div[3]/div/div/div[2]/div[2]/div[1]/form/div[3]/button[1]')[0].click()
            sleep(3)

            links = driver.find_elements(By.ID, 'table')

            anchor_links = links[0].find_elements(By.CSS_SELECTOR, 'a')
            pdf_links = [x.get_attribute('href').strip() for x in anchor_links]
            print(pdf_links)
            for pdf_url in pdf_links:
                try:
                    response = requests.get(pdf_url, timeout=30)
                    if response.status_code == 200:
                        # Get the content of the response (the PDF file)
                        pdf_content = response.content
                        folder_path = rf"D:\form_20\Haryana\Vidhansabha\2019"
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

        # Call the function
if __name__ == '__main__':
    form_20()




