from time import sleep
from selenium import webdriver

baseurl = ""
options = webdriver.ChromeOptions()
options.add_argument("--incognito")

desiredCapabilities caps = options.to_capabilities()

driver = webdriver.Chrome(desired_capabilities=caps)
driver.get('https://twitter.com/')