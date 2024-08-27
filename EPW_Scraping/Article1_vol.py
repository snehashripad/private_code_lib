from hashlib import new

import undetected_chromedriver as webdriver
from selenium import webdriver
import time
import os
import json
from selenium.webdriver.common.by import By
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

clean_list = []


def write_json(obj, filepath, ensure_ascii=False):
    with open(filepath, "w", encoding="utf8", errors='ignore') as f:
        json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)


def update_clean_list(article_schema):
    clean_list.append(article_schema)
    write_json(clean_list, rf'C:\temp\Article_1.json')


def kill_all_open_chrome_instances():
    os.system('taskkill /f /fi "imagename eq chrome*')


if __name__ == '__main__':
    kill_all_open_chrome_instances()
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument(rf"--user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data")
    options.add_argument(f"--profile-directory=Profile 3")
    options.add_experimental_option('prefs', {"download.default_directory": "C:\temp\data",
                                              "download.prompt_for_download": False,
                                              "plugin.always_open_pdf_externally": True})

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(options=options)



    for year in range(2023, 2024):
        for click in range(1, 201):
            driver.get(rf"https://www.epw.in/journal/{year}/{click}")
            time.sleep(3)

            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="block-system-main"]/div/div/div/div/div')))
            # title_links = driver.find_elements(by=By.XPATH, value=f'//*[@id="block-system-main"]/div/div/div/div/div')
            try:
                title_links = driver.find_elements(by=By.XPATH,
                                                   value=f'//*[@id="block-system-main"]/div/div/div/div/div')
                article_links = driver.find_elements(By.CSS_SELECTOR,'.block-inner .views-field-title a')
                links = [x.get_attribute('href').strip() for x in article_links]
                links = set(links)


                for link in links:
                    driver.get(link[7])

                    print(link)
                    time.sleep(3)


                    article_schema = {}
                    article_schema['year'] = driver.find_elements(by=By.XPATH,
                                                                  value='//*[@id="block-block-43--2"]/div/div/div[2]/div[1]/div/div/a')[
                        0].text.split(',')[3]
                    article_schema['Title'] = driver.find_elements(by=By.XPATH, value='//*[@id="page-title"]/span[1]')[
                        0].text

                    try:
                        article_schema['Subtitle'] = \
                            driver.find_elements(by=By.XPATH, value='//*[@class = "article_summary"]')[0].text
                        article_schema['Content'] = \
                            driver.find_elements(by=By.XPATH, value='//*[@class = "body_content"]')[0].text


                    except:
                        article_schema['Subtitle'] = ''
                        article_schema['Content'] = ''
                    article_schema['Journal_Details'] = driver.find_elements(by=By.XPATH,
                                                                             value=f'//*[@id="block-block-43--2"]/div/div/div[2]/div[1]/div/div/a')[
                        0].text
                    article_schema['Update'] = \
                        driver.find_elements(by=By.XPATH, value=f'//*[@id="block-block-43--2"]/div/div/div[2]/div[2]')[
                            0].text
                    article_schema['Tags'] = driver.find_elements(by=By.XPATH, value='//*[@class="tag_container"]')[
                        0].text.replace('\n', ', ')
                    download_pdf = \
                        driver.find_elements(by=By.XPATH, value=f"//a[contains(text(),'Download PDF Version')]")[0]
                    link = download_pdf.get_attribute('href')
                    article_schema['PDF_Link'] = link


                    driver.implicitly_wait(5)
                    driver.back()
                    # update_clean_list(article_schema)

            except BaseException:
                print("item is not clickable")
                continue
            finally:
                driver.back()

                # article_schema = {}
                # article_schema['Title'] = driver.find_elements(by=By.XPATH, value=f'//*[
                # @id="page-title"]/span[1]')[0].text ' \
                #                          'article_schema['Subtitle'] = driver.find_elements(by=By.XPATH,
                # value='//*[@id="node-162592"]/div/div[2]/div/div/div/p/i')[0].text article_schema[
                # 'Journal_Details'] = driver.find_elements(by=By.XPATH, value='//*[
                # @id="block-block-43--2"]/div/div/div[2]/div[1]/div/div/a')[0].text article_schema['Content'] =
                # driver.find_elements(by=By.XPATH, value='//*[@id="node-162592"]/div/div[3]/div/div/div')[0].text
                # article_schema['Update'] = driver.find_elements(by=By.XPATH, value='//*[
                # @id="block-block-43--2"]/div/div/div[2]/div[2]')[0].text # article_schema['Tags'] print(
                # article_schema) # update_clean_list(article_schema) print(driver.title)
                # time.sleep(5)
