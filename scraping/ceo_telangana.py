from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Set the path to your ChromeDriver executable
chrome_driver_path = r'/Drivers/chromedriver.exe'

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

url = 'https://ceotserms2.telangana.gov.in/TS_ERODETAILS/BLO_Details.aspx'
driver.get(url)


def ceo_telangana_scraping(options=None):
    driver = webdriver.Chrome(service=service, options=options)
    url = 'https://ceotserms2.telangana.gov.in/TS_ERODETAILS/BLO_Details.aspx'
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(5)

    options = Options()
    options.headless = True

    # Assuming the districts are listed in a dropdown with id 'district_dropdown'
    district_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'district_dropdown')))
    district_options = district_dropdown.find_elements(By.TAG_NAME, "option")
    district_names = [option.text for option in district_options]

    for district_name in district_names:
        # Select the district from the dropdown
        district_dropdown = driver.find_element(By.ID, 'district_dropdown')
        district_dropdown.send_keys(district_name)

        # Wait for the constituencies to load (replace 'constituency_dropdown' with the correct ID if needed)
        constituency_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'constituency_dropdown')))
        constituency_options = constituency_dropdown.find_elements(By.TAG_NAME, "option")
        constituency_names = [option.text for option in constituency_options]

        district_data = {}

        for constituency_name in constituency_names:
            # Select the constituency from the dropdown
            constituency_dropdown = driver.find_element(By.ID, 'constituency_dropdown')
            constituency_dropdown.send_keys(constituency_name)

            # Wait for the table to load (replace 'table_id' with the correct ID of the table)
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'table_id')))

            # Scrape table data and store it in a list of dictionaries
            rows = table.find_elements(By.TAG_NAME, "tr")
            constituency_data = []
            for row in rows[1:]:  # Skip the header row
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = {
                    "field1": cells[0].text,
                    "field2": cells[1].text,
                    # Add more fields as needed based on the table columns
                }
                constituency_data.append(row_data)

            district_data[constituency_name] = constituency_data

        all_data[district_name] = district_data


if __name__ == '__main__':
    ceo_telangana_scraping()
