import os
from time import sleep
import srsly
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException


def save_html_from_element(driver, element_id, file_path):

    data_div = driver.find_element(By.ID, element_id)
    html = data_div.get_attribute("outerHTML")
    with open(file_path, 'w', encoding='utf8') as f:
        f.write(html)
    sleep(2)


def find_elements(driver, selector_type, selector):

    selector_type = selector_type.lower()

    if selector_type == 'css':
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
    elif selector_type == 'xpath':
        elements = driver.find_elements(By.XPATH, selector)
    elif selector_type == 'id':
        elements = driver.find_elements(By.ID, selector)
    elif selector_type == 'name':
        elements = driver.find_elements(By.NAME, selector)
    elif selector_type == 'class':
        elements = driver.find_elements(By.CLASS_NAME, selector)
    elif selector_type == 'tag':
        elements = driver.find_elements(By.TAG_NAME, selector)
    elif selector_type == 'link_text':
        elements = driver.find_elements(By.LINK_TEXT, selector)
    elif selector_type == 'partial_link_text':
        elements = driver.find_elements(By.PARTIAL_LINK_TEXT, selector)
    else:
        raise ValueError(f"Unsupported selector type: {selector_type}")

    return elements


def click_option(driver, xpath, value):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath.format(value))))
            driver.execute_script("arguments[0].scrollIntoView(true);", option)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath.format(value))))
            option.click()
            return
        except (StaleElementReferenceException, TimeoutException, WebDriverException) as e:
            print(f"Error clicking option {value}: {e}")
            print(f"XPath of the element: {xpath.format(value)}")
            print("Retrying...")
            retries += 1
            sleep(5)
            driver.refresh()


def format_option_text(text):
    return text.replace("'", "\\'")


def click_habitation_link(driver):
    try:
        link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'CPHPage_lblHab')))
        link.click()
    except TimeoutException:
        print("Habitation link not found. Trying again...")
        driver.refresh()
        sleep(2)
        return False
    return True






