from time import sleep
import re

import srsly
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

path = r"C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe"
options = Options()

options.add_experimental_option('detach', True)
service = Service(executable_path=path)


def contesting_sarpanch(driver):
    rows = driver.find_elements(by=By.XPATH, value=f'//*[@id="tabs-1"]/div/table[1]/tbody/tr')
    sleep(3)
    candidate = []
    count = len(rows)

    for item in range(1, count + 1):
        try:
            dict_ = {}
            dict_['name'] = \
            driver.find_elements(by=By.XPATH, value=f'//*[@id="tabs-1"]/div/table[1]/tbody/tr[{item}]/td[5]')[0].text
            dict_['phone_number'] = \
            driver.find_elements(by=By.XPATH, value=f'//*[@id="tabs-1"]/div/table[1]/tbody/tr[{item}]/td[16]')[0].text
            candidate.append(dict_)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, f'//*[@id="tabs-1"]/div/table[1]/tbody/tr[{item}]/td[16]')))
        except:
            continue

    print(candidate)
    return candidate


clean_list = []


def update_clean_list(gram_panch_schema):
    clean_list.append(gram_panch_schema)
    srsly.write_json(rf'C:\temp\gp_r_sikar.json', clean_list)


def gp_raj_scraping():
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(r'https://sec.rajasthan.gov.in/grampanchayatdetails.aspx')
    driver.maximize_window()
    sleep(5)

    # ele_type = driver.find_elements(by=By.XPATH, value='//*[@id="ContentPlaceHolder1_DropDownListElection"]')
    # sleep(3)
    # # for type in ele_type

    # click on election duration
    ele_duration = driver.find_elements(by=By.XPATH, value='//*[@id="ContentPlaceHolder1_DropDownListPeriod"]')[
                       0].text.split('\n')[1:]
    for duration in ele_duration:
        duration = duration.strip()
        driver.find_elements(by=By.XPATH,
                             value=f'//*[@id="ContentPlaceHolder1_DropDownListPeriod"]/option[text() = "{duration}"]')[
            0].click()
        print(duration)
        sleep(3)

        # District
        district = driver.find_elements(by=By.XPATH, value=f'//*[@id="ContentPlaceHolder1_DistrictDropDownList"]')[
                       0].text.split("\n")[30:]
        sleep(3)
        district = [x.strip() for x in district if x != "  "]
        for dist in district:
            driver.find_elements(by=By.XPATH,
                                 value=f'//*[@id="ContentPlaceHolder1_DistrictDropDownList"]/option[text() = "{dist}"]')[
                0].click()
            print(dist)
            sleep(3)

            # Panchayat Samiti
            panchayat_samiti = driver.find_elements(by=By.XPATH, value=f'//*[@id="PanchayatSamitiDropDownList"]')[
                                   0].text.split("\n")[3:]
            sleep(5)
            panchayat_samiti = [x.strip() for x in panchayat_samiti if x != "  "]
            for samiti in panchayat_samiti:
                samiti = samiti.strip()
                if samiti == "":
                    break
                else:
                    driver.find_elements(by=By.XPATH,
                                         value=f'//*[@id="PanchayatSamitiDropDownList"]/option[text() = "{samiti}"]')[
                        0].click()
                    print(samiti)
                    sleep(5)

                # // *[ @ id = "ContentPlaceHolder1_GramPanchayatdrpdwn"]
                # Gram Panchayat
                # gram_panchayat = driver.find_elements(by=By.XPATH, value= f'//*[@id="ContentPlaceHolder1_GramPanchayatdrpdwn"]')[0].text.split("\n")[1:]
                gram_panchayat_len = len(driver.find_elements(by=By.XPATH,
                                                              value=f'//*[@id="ContentPlaceHolder1_GramPanchayatdrpdwn"]/option')[
                                         1:])
                # gram_panchayat = ''
                for grams in range(gram_panchayat_len):
                    gram_panchayats = driver.find_elements(by=By.XPATH,
                                                           value=f'//*[@id="ContentPlaceHolder1_GramPanchayatdrpdwn"]/option')[
                                      1:]
                    grm = gram_panchayats[grams]
                    grm_text = grm.text
                    print(grm_text)
                    gram_panchayat_schema = {}
                    grm.click()

                    # click on submit button
                    web_ele = driver.find_elements(by=By.ID, value=f'ContentPlaceHolder1_btnSubmit')[0]
                    action = ActionChains(driver)
                    action.move_to_element(web_ele).click().perform()

                    sleep(5)

                    gram_panchayat_schema['Election_duration'] = duration
                    gram_panchayat_schema['District'] = dist
                    gram_panchayat_schema['Panchayat_samiti'] = samiti
                    gram_panchayat_schema['Gram_panchayat'] = grm_text
                    gram_panchayat_schema['cont_sarpanch'] = contesting_sarpanch(driver)

                    # print(gram_panchayat_schema)
                    update_clean_list(gram_panchayat_schema)
                    # try:
                    #     driver.close()
                    # except:
                    #     continue


if __name__ == '__main__':
    gp_raj_scraping()
