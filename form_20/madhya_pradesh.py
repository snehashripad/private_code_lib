import os
from time import sleep

import requests
from selenium import webdriver
from selenium.common import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


path = r"C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe"
_options = Options()
_options.add_argument("--window-size=1920,1080")

_options.add_experimental_option('detach', True)
service = Service(executable_path=path)

def mp_form_20():
    driver = webdriver.Chrome(service=service, options=_options)
    driver.get(r"https://ceomadhyapradesh.nic.in/AssemblyElection2018.aspx")
    sleep(2)
    district = driver.find_elements(By.XPATH, f'//*[@id="AnxE2"]/div[2]')[0].text.split('\n')[2:3]
    for dist in district:
        dist = dist.strip()
        driver.find_elements(by=By.XPATH, value=f'//*[@id="ctl00_ContentPlaceHolder1_ddlDist"]/option[text() = "{dist}"]')[0].click()
        print(dist)
        sleep(3)
        Assembly = driver.find_elements(By.XPATH, value=f'//*[@id="aspnetForm"]/div[3]/section/div/div/div/div/table/tbody/tr[3]/td[2]/div[6]/div[3]')[0].text.split('\n')[3:4]
        for item in Assembly:
            item = item.strip()
            driver.find_elements(By.XPATH, value=f'//*[@id="ctl00_ContentPlaceHolder1_ddlAC"]/option[text() = "{item}"]')[0].click()
            sleep(5)
            driver.find_elements(By.ID, 'ctl00_ContentPlaceHolder1_btnForm20')[0].click()
            sleep(5)
            try:
                driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'body > embed'))
                sleep(5)

            except NoAlertPresentException:
                pass
            driver.back()


if __name__ == "__main__":
    mp_form_20()