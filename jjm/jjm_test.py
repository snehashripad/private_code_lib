import os
from time import sleep
import srsly
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException

WORKING_DIR = fr'D:\jjm'
STATE_NAME = 'Maharashtra'


def click_option(driver, xpath, value):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath.format(value))))
            driver.execute_script("arguments[0].scrollIntoView(true);", option)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath.format(value))))
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



def recur_scrape(current_dir):
    try:
        os.makedirs(current_dir, exist_ok=True)
    except PermissionError:
        print("Permission denied: Unable to create directories.")
        return
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(rf"https://ejalshakti.gov.in/JJM/JJM/Public/Profile/VillageProfile.aspx")
    sleep(5)
    driver.maximize_window()

    state = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddState")]')[0].text.split('\n')[21:22]
    for item in state:
        item = item.strip()
        list1 = [state]
        srsly.write_json(fr'{current_dir}\state.json', list1)

        click_option(driver, '//*[contains(@id, "CPHPage_ddState")]/option[text()="{}"]'.format(item), item)
        sleep(3)
        print(item)

        district = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddDistrict")]')[0].text.split('\n')[19:20]
        for dist in district:
            dist = dist.strip()
            district_dir = os.path.join(current_dir, str(dist))

            if not os.path.exists(district_dir):
                os.makedirs(district_dir)
            list2 = [district]
            srsly.write_json(fr'{district_dir}\district.json', list2)

            click_option(driver, '//*[contains(@id, "CPHPage_ddDistrict")]/option[text()="{}"]'.format(dist), dist)
            sleep(2)
            print(dist)

            block = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddBlock")]')[0].text.split('\n')[1:]
            for blk in block:
                blk = blk.strip()
                block_dir = os.path.join(district_dir, str(blk))

                if not os.path.exists(block_dir):
                    os.makedirs(block_dir)
                list3 = [block]
                srsly.write_json(fr'{block_dir}\block.json', list3)

                click_option(driver, '//*[contains(@id, "CPHPage_ddBlock")]/option[text()="{}"]'.format(blk), blk)
                print(blk)
                sleep(2)

                panchayat = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddPanchayat")]')[0].text.split(
                    '\n')[1:]
                for index, panc in enumerate(panchayat):
                    panc = panc.strip()
                    panchayat_dir = os.path.join(block_dir, str(panc))

                    if not os.path.exists(panchayat_dir):
                        os.makedirs(panchayat_dir)
                    list4 = [panchayat]
                    srsly.write_json(fr'{panchayat_dir}\panchayat.json', list4)

                    # Construct the XPath for panchayat option
                    formatted_panc = format_option_text(panc)
                    xpath = '//*[contains(@id, "CPHPage_ddPanchayat")]/option[normalize-space(text())="{}"]'
                    click_option(driver, xpath, formatted_panc)
                    sleep(5)
                    print("panchayat_name", index, panc)

                    village = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddVillage")]')[0].text.split(
                        '\n')[1:]
                    for index, vil in enumerate(village):
                        vil1 = vil.strip().replace('/', '_')
                        village_dir = os.path.join(panchayat_dir, str(vil1))

                        if not os.path.exists(village_dir):
                            os.makedirs(village_dir)
                        list5 = [village]
                        srsly.write_json(fr'{village_dir}\vil1.json', list5)
                        formatted_vil = format_option_text(vil)
                        xpath = '//*[contains(@id, "CPHPage_ddVillage")]/option[normalize-space(text())="{}"]'
                        click_option(driver, xpath, formatted_vil)

                        sleep(1)

                        print("village_name", index, vil)

                        # click on show button
                        driver.find_elements(By.ID, 'CPHPage_btnShow')[0].click()
                        sleep(3)

                        if not click_habitation_link(driver):
                            # If habitation link was not found, skip further execution
                            return

                        data_div = driver.find_element(By.ID, 'CPHPage_divgrid')
                        html = data_div.get_attribute("outerHTML")
                        file_name = fr'{village_dir}\{vil1}.html'
                        with open(file_name, 'w', encoding='utf8') as f:
                            f.write(html)
                            sleep(2)


if __name__ == '__main__':
    current_dir = fr'{WORKING_DIR}\{STATE_NAME}'
    recur_scrape(current_dir)
