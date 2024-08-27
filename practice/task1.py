import time
from requests import Session
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

time.sleep(2)
path = r"/Drivers/chromedriver.exe"
##########################################################################################
# options = webdriver.ChromeOptions()
# options.add_argument("--window-size=1920,1080")
# _path = r"C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe"
# driver = webdriver.Chrome(options=options)
# driver.service.executable_path = _path
# time.sleep(2)
#
# driver.get(r"https://twitter.com/i/flow/login?redirect_after_login=%2Flogin%3Flang%3Den")

_options = Options()
_options.add_argument("--window-size=1920,1080")

_options.add_experimental_option('detach', True)
service = Service(executable_path=path)


#######################################################################################
def launchBrowser():
    driver = webdriver.Chrome(service=service, options=_options)

    # # driver.get(r"https://www.makemytrip.com/")
    driver.get(r"https://twitter.com/home")


launchBrowser()
time.sleep(2)
#########################################################################################
'''
with Session() as s:
    site = s.get("https://twitter.com/i/flow/login?redirect_after_login=%2F%3Flang%3Den")
    bs_content = bs(site.content, "html.parser")
    token = bs_content.find("input", {"name":"csrf_token"})["value"]
    login_data = {"username":"admin","password":"12345", "csrf_token":token}
    s.post("https://twitter.com/i/flow/login?redirect_after_login=%2F%3Flang%3Den",login_data)
    home_page = s.get("https://twitter.com/")
    print(home_page.content)
'''
############################################################################################3
