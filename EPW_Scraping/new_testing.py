import random
from hashlib import new

from selenium import webdriver
import time
import os
import json
import urllib3

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def write_json(obj, filepath, ensure_ascii=False):
    with open(filepath, "w", encoding="utf8", errors='ignore') as f:
        json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)


clean_list = []

def update_clean_list(article_schema):
    clean_list.append(article_schema)
    write_json(clean_list, rf'D:\data\2007\Article_2007.json')


def get_title(driver):
    title = driver.find_elements(by=By.XPATH, value='//*[@id="page-title"]/span[1]')[0]
    try:
        title_ = title.text
    except:
        action = ActionChains(driver)
        title = driver.find_elements(by=By.XPATH, value='//*[@id="page-title"]/span[1]')[0]
        action.move_to_element(title).perform()
        title_ = title.text
    else:
        pass

    return title_


def get_tags(driver):
    try:
        tags = driver.find_elements(by=By.XPATH, value='//*[@class="tag_container"]')[0]
        tags_ = tags.text.replace('\n', ', ')
    except:
        tags = driver.find_elements(by=By.XPATH, value='//*[@class="tags"]')[0]
        tags_ = tags.text.replace('\n', ', ')
    else:
        pass
    return tags_


def get_pdf_link(driver):
    try:
        download_pdf_ = \
            driver.find_elements(by=By.XPATH, value=f'//*[@id="block-block-144--2"]/div/div/div/div/div/span/a')[0]
        link_ = download_pdf_.get_attribute('href')

    except:
        download_pdf_ = driver.find_elements(by=By.XPATH, value=f'//a[contains(text(),"Download PDF")]')[0]
        link_ = download_pdf_.get_attribute('href')



    download_pdf_.click()

    return link_


def get_year(driver):
    try:
        year = driver.find_elements(by=By.XPATH, value='//*[@id="block-block-43--2"]/div/div/div[2]/div[1]/div/div/a')[
            0].text.split(',')[3]
    except:
        year = driver.find_elements(driver.find_elements(by=By.XPATH, value=f'//*[@class="vol"]')[0].text.split(',')[3])

    return year


def get_journal_details(driver):
    try:
        journal_details = driver.find_elements(by=By.XPATH,
                                               value=f'//*[@id="block-block-43--2"]/div/div/div[2]/div[1]/div/div/a')[
            0].text
    except:
        journal_details = driver.find_elements(by=By.XPATH, value=f'//*[@class="vol"]')[
            0].text

    return journal_details


def get_Update(driver):
    try:
        update = \
            driver.find_elements(by=By.XPATH, value=f'//*[@id="block-block-43--2"]/div/div/div[2]/div[2]')[
                0].text
    except:
        update = driver.find_elements(by=By.XPATH, value=f'//*[@class="date"]')[0].text
    return update


def get_all_links(driver):

    article_links = driver.find_elements(By.CSS_SELECTOR, '.block-inner .views-field-title a')
    # for item in article_links:
    links = [x.get_attribute('href').strip() for x in article_links]

    for index, href in enumerate(links):

        if href == 'https://www.epw.in/book-store':
            links.remove(href)

        else:
            driver.get(href)
            print(index, href)
            article_schema = {'Article_link': href}
            try:
                article_schema['Title'] = get_title(driver)
            except:
                num = random.random()
                article_schema['Title'] = num

            try:
                article_schema['year'] = get_year(driver)
            except:
                num = random.random()
                article_schema['year'] = num

            try:
                article_schema['SubTitle'] = driver.find_elements(by=By.XPATH, value='//*[@class = "article_summary"]')[
                    0].text
            except:
                article_schema['SubTitle'] = ""
            else:
                pass
            try:
                article_schema['Journal_Details'] = get_journal_details(driver)

            except:
                article_schema['Journal_Details'] = ""

            try:
                article_schema['Update'] = get_Update(driver)

            except:
                article_schema['Update'] = ""

            try:
                article_schema['Tags'] = get_tags(driver)
            except:
                article_schema['Tags'] = ""

            try:
                article_schema['Content'] = driver.find_elements(by=By.XPATH, value='//*[@class = "body_content"]')[
                    0].text

            except:
                article_schema['Content'] = ''

            try:
                article_schema['PDF_LINK'] = get_pdf_link(driver)
                article_schema['pdf_file'] = article_schema['PDF_LINK'].split('/')[-1].strip()
            except:
                article_schema['PDF_LINK'] = ""

            print(article_schema)
            update_clean_list(article_schema)
    driver.back()


# fr"D:\data.pdf"


def kill_all_open_chrome_instances():
    os.system('taskkill /f /fi "imagename eq chrome*')


if __name__ == '__main__':

    # download_pdf(f"https://www.epw.in/system/files/pdf/2023_58/45-46/ED_LVIII_45-46_181123_A%2070-hour%20Workweek.pdf",rf"D:\pdf\002.pdf")

    kill_all_open_chrome_instances()
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument(rf"--user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data")
    options.add_argument(f"--profile-directory=Profile 5")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('prefs', {"download.default_directory": fr"D:\data\2016.pdf",
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "plugin.always_open_pdf_externally": True
                                              })

    urllib3.disable_warnings()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(options=options)
    # driver.set_page_load_timeout(90)

    # Load the URL and get the page source
    driver.implicitly_wait(6)


    driver.get(f'https://www.epw.in/journal/epw-archive')
    driver.implicitly_wait(2)
    year_links = driver.find_elements(By.CSS_SELECTOR, "span[class='fieldset-legend']")[16:17]
    year = year_links[0].text.split('\n')[1]

    # create_new_folder()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='fieldset-legend']")))

    for index, item in enumerate(year_links):
        print(index, item.text)
        actions = ActionChains(driver)
        actions.move_to_element(item).click().perform()
        driver.implicitly_wait(5)
        list = driver.find_elements(By.CSS_SELECTOR, "div[class='fieldset-wrapper']")[16:]
        vol_links = list[0].find_elements(By.CSS_SELECTOR, "a")
        links = [x.get_attribute('href').strip() for x in vol_links][0:]
        for index, item in enumerate(links):
            print(item)

            driver.get(item)
            get_all_links(driver)
            driver.back()

# fr"D:\data.pdf"


# def get_year_(driver):
#     year_links = driver.find_elements(By.CSS_SELECTOR, "span[class='fieldset-legend']")[5:6]
#     year = year_links[0].text.split('\n')[1]
#
#     # create_new_folder()
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='fieldset-legend']")))
#
#
#
#     for index, item in enumerate(year_links):
#         print(index, item.text)
#         actions = ActionChains(driver)
#         actions.move_to_element(item).click().perform()
#         driver.implicitly_wait(5)
#         list = driver.find_elements(By.CSS_SELECTOR, "div[class='fieldset-wrapper']")[5:]
#         vol_links = list[0].find_elements(By.CSS_SELECTOR, "a")
#         links = [x.get_attribute('href').strip() for x in vol_links][0:]
#         for index, item in enumerate(links):
#             print(item)
#
#             driver.get(item)
#             get_all_links(driver)
#             driver.back()
#     return year


# for link in vol_links:
#     time.sleep(5)
#     link.click()
#     get_all_links(driver)
#     driver.back()
# driver.back()

# get_all_links(driver)

# get_all_links(driver)
# for year in range(2023, 2024):
#     for click in range(1, 201):
#         driver.get(rf"https://www.epw.in/journal/{year}/{click}")
#         get_all_links(driver)
