from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

path = r"/Drivers/chromedriver.exe"
options = Options()
# options.headless = True  # Set to true so browser window is not displayed
options.add_experimental_option('detach', True)
service = Service(executable_path=path)

driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1280, 720)
driver.get('https://www.facebook.com/BSYBJP/')

time.sleep(2)