from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to your ChromeDriver executable
chrome_driver_path = r'C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe'

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

url = 'https://www.ghmc.gov.in/KeyContacts.aspx'
driver.get(url)
try:
    mayor = driver.find_elements(by=By.XPATH, value=f'//*[@id="headingOneone"]/h5/a')[0]
    mayor.click()
    driver.implicitly_wait(5)
    mayor.click()
    driver.implicitly_wait(5)
    try:
        wait = WebDriverWait(driver,40)  # Increase the wait time to 20 seconds
        element_present = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Zonal Commissioners')))
        element_clickable = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Zonal Commissioners')))
        element_clickable.click()

    except Exception as e:
        print("Error msg: ", str(e))
        print("Page Source:", driver.page_source)

finally:
    driver.quit()
