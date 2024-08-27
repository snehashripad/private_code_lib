import re

import srsly
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pathlib import Path
import requests

path = r"/Drivers/chromedriver.exe"
_options = Options()
_options.add_argument("--window-size=1920,1080")

_options.add_experimental_option('detach', True)
service = Service(executable_path=path)

##########################################################################################################
def rev_coll(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    sleep(3)
    # click on revenue collection
    driver.find_elements(by=By.XPATH, value=f'//*[@id="accordionExample"]/div[4]/div[1]/button')[0].click()
    sleep(3)
    # click on view all button
    try:
        button = driver.find_elements(by=By.XPATH, value=f'//*[@id="gp-revenue-collection__ID"]/div/div[2]/button')[0]
        type(button)
        button.click()
        sleep(3)
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        rc = driver.find_elements(by=By.XPATH, value=f'//*[@id="gp_rev_collection_row__ID"]/div/div')
        sleep(4)
    except:
        rc = driver.find_elements(by=By.XPATH, value=f'//*[@id="gp_rev_collection_row__ID"]/div/div')
        sleep(4)


    lis = []
    for item in rc:
        # lis.append(item)
        dic_rc = {}
        dic_rc['village_name'] = item.text.split('\n')[0].split(':')[1]
        dic_rc['properties'] = item.text.split('\n')[1].split()[0]
        dic_rc['tot_demand'] = item.text.split('\n')[2].split(':')[1]
        dic_rc['arrears'] = item.text.split('\n')[3].split(':')[1]
        dic_rc['current_demand'] = item.text.split('\n')[4].split(':')[1]
        dic_rc['tot_demand_coll'] = item.text.split('\n')[6]
        dic_rc['tot_bal'] = item.text.split('\n')[8]
        print(dic_rc['village_name'])
        lis.append(dic_rc)
        item.click()
        sleep(3)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    sleep(3)

    all_links = driver.find_elements(by=By.XPATH,
                                     value=f'//*[@id="village-properties-table__ID_paginate"]/ul/li')
    num_of_pages = int(all_links[-2].text)
    clean_list_ = []
    for _ in range(1, num_of_pages+1):
        clean_list_.append(read_rows(driver))
        try:
            next_page = driver.find_elements(by=By.XPATH, value=f"//a[text()='Next']")[0]
            next_page.click()
        except:
            break
    return clean_list_
# continue



def read_rows(driver):
    rows = driver.find_elements(by=By.XPATH, value=f'//*[@id="village-properties-table__ID"]/tbody/tr')
    count = len(rows)
    sleep(3)
    clean_list = []
    for i in range(1, count + 1):
        dict_property_details = {}
        dict_property_details['srl_no'] = driver.find_element(by=By.XPATH,
                                                              value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[1]').text
        dict_property_details['pro_id'] = driver.find_element(by=By.XPATH,
                                                              value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[2]').text
        dict_property_details['pro_num'] = driver.find_element(by=By.XPATH,
                                                               value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[3]').text
        dict_property_details['pro_owner_name'] = driver.find_element(by=By.XPATH,
                                                                      value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[4]').text
        dict_property_details['arrear_rs'] = driver.find_element(by=By.XPATH,
                                                                 value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[5]').text
        dict_property_details['curr_demand'] = driver.find_element(by=By.XPATH,
                                                                   value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[6]').text
        dict_property_details['tot_demand'] = driver.find_element(by=By.XPATH,
                                                                  value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[7]').text
        dict_property_details['tot_demand_collection'] = driver.find_element(by=By.XPATH,
                                                                             value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[8]').text
        dict_property_details['tot_bal'] = driver.find_element(by=By.XPATH,
                                                               value=f'//*[@id="village-properties-table__ID"]/tbody/tr[{i}]/td[9]').text
        clean_list.append(dict_property_details)
    return clean_list



#########################################################################################################
def _meetings(driver):
    # driver.implicitly_wait(5)
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    sleep(3)
    driver.find_elements(by=By.XPATH, value=f'//*[@id="accordionExample"]/div[3]/div[1]/button')[0].click()
    sleep(3)
    try:
        # click on view all button
        driver.find_elements(by=By.XPATH, value=f'//*[@id="comp-meet_tab__ID"]/div[2]')[0].click()
        sleep(3)
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        sleep(2)
        meetings = driver.find_elements(by=By.XPATH, value=f'//*[@id="comp-meet_tab__ID"]/div/div')
        sleep(3)
    except:
        meetings = driver.find_elements(by=By.XPATH, value=f'//*[@id="comp-meet_tab__ID"]/div/div')

        sleep(3)
        # '//*[@id="comp-meet_tab__ID"]/div/div[2]'
    # gp_meetings = []
    static_link = 'https://panchatantra.karnataka.gov.in/USER_MODULE/ajax/downloadDoc/'
    for meet in meetings:
        # gp_meetings.append(meet)

        button_ele_proceeding = driver.find_elements(by=By.XPATH, value=f'//*[@id="comp-meet_tab__ID"]/div/div[1]/div/div/div/div/div/cite/div/button')[0]
        # get the value of the desired attribute
        sleep(3)
        att_value = button_ele_proceeding.get_attribute("onclick")
        sleep(2)
        dyna_link = att_value.split(",")[2]+'/'+ att_value.split(",")[3]
        sleep(2)
        try:
            dict_meet = {}
            dict_meet['meet_name'] = meet.text.split('\n')[0] + meet.text.split('\n')[1]
            dict_meet['date'] = meet.text.split('\n')[2]
            dict_meet['venue'] = meet.text.split('\n')[4]
            sleep(2)
            dict_meet['proceedings_'] = static_link + dyna_link
            sleep(2)
        except:
            continue
    return _meetings


##################################################################################################################
def staff_details(driver):
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    sleep(3)
    driver.find_elements(by=By.XPATH, value='//*[@id="accordionExample"]/div[2]/div[1]/button')[0].click()
    sleep(5)
    try:
        # click on view all button
        driver.find_elements(by=By.XPATH, value='//*[@id="gp-all-staff__ID"]/div/div[2]/button')[0].click()
        sleep(5)
        handles = driver.window_handles
        # swtich to child window
        driver.switch_to.window(handles[2])
        sleep(3)
        staff_members = driver.find_elements(by=By.XPATH, value=f'//*[@id="gp-all-staff-row__ID"]/div')
        sleep(5)
    except:
        staff_members = driver.find_elements(by=By.XPATH, value=f'//*[@id="gp-all-staff-row__ID"]/div')
        sleep(5)
    staff_mem = []
    for item in staff_members:
        # staff_mem.append(item.text)
        try:
            dict_staff = {}
            dict_staff['name'] = item.text.split('\n')[0].split('(')[0]
            dict_staff['posi'] = item.text.split('\n')[0].split('(')[1].replace(')', '')
            dict_staff['ph_no'] = item.text.split('\n')[1]
            staff_mem.append(dict_staff)
        except:
            continue
    return staff_mem


##################################################################################################################
def ele_rep_details(driver):
    driver.find_element(by=By.XPATH, value='//*[@id="accordionExample"]/div[1]/div[1]/button').click()
    sleep(2)
    members = []

    try:
        # click on view all button
        button = driver.find_elements(by=By.XPATH, value='//*[@id="gp-Er-staff__ID"]/div/div[2]/button')[0]
        type(button)
        button.click()
        sleep(5)

        # get the window handles
        handles = driver.window_handles

        # swtich to child window
        driver.switch_to.window(handles[1])
        representatives = driver.find_elements(by=By.XPATH, value='//*[@id="er-staff-row__ID"]/div')

    except:
        representatives = driver.find_elements(by=By.XPATH, value='//*[@id="er-staff-row__ID"]/div')
    for item in representatives:
        # list_.append(item.text)
        try:
            dict_ = {}
            dict_['name'] = item.text.split('\n')[0].split('(')[0]
            dict_['position'] = item.text.split('\n')[0].split('(')[1].replace(')', '')
            dict_['Phone_no'] = item.text.split('\n')[1]
            members.append(dict_)

        except:
            continue
    return members


com_list = []


def update_clean_list(gram_panch_schema, dist, tal):
    com_list.append(gram_panch_schema)
    srsly.write_json(rf'C:\temp\rev_collection\{dist}_{tal}.json', com_list)
    # srsly.write_json()


####################################################################################################################################
def gp_scraping():
    driver = webdriver.Chrome(service=service, options=_options)
    driver.get(r"https://panchatantra.karnataka.gov.in/USER_MODULE/userLogin/loadPanchamitra")
    driver.maximize_window()
    sleep(2)

    district = driver.find_elements("xpath", '//*[@id="flt_zp__Id"]')[0].text.split('\n')[1:]
    for dist in district:
        dist = dist.strip()
        handles = driver.window_handles
        driver.switch_to.window(handles[0])
        driver.find_elements(by=By.XPATH, value=f'//*[@id="flt_zp__Id"]/option[text() = "{dist}"]')[0].click()
        print(dist)
        sleep(3)
        # taluk
        taluk = driver.find_elements(by=By.XPATH, value="//*[@id='flt_tp__Id']")[0].text.split('\n')[1:]
        sleep(2)
        for tal in taluk:
            tal = tal.strip()
            handles = driver.window_handles
            driver.switch_to.window(handles[0])
            driver.find_elements(by=By.XPATH, value=f'//*[@id="flt_tp__Id"]/option[text() = "{tal}"]')[0].click()
            print(tal)
            sleep(3)
            # gram_panchayat
            gram_panch = driver.find_elements(by=By.XPATH, value=f'//*[@id="flt_gp__Id"]')[0].text.split('\n')[1:]
            for _gp in gram_panch:
                _gp = _gp.strip()
                gram_panch_schema = {}
                handles = driver.window_handles
                driver.switch_to.window(handles[0])
                driver.find_elements(by=By.XPATH, value=f'//*[@id="flt_gp__Id"]/option[text() ="{_gp}"]')[0].click()
                print(_gp)
                sleep(5)

                # click on search button
                # handles = driver.window_handles
                # driver.switch_to.window(handles[0])
                driver.find_element(by=By.XPATH, value=f'//*[@id="gp_dtl_searchBtn__ID"]').click()
                sleep(5)

                gram_panch_schema['district'] = dist
                gram_panch_schema['tal'] = tal
                gram_panch_schema['gp'] = _gp
                # gram_panch_schema['repre'] = ele_rep_details(driver)
                # gram_panch_schema['staff'] = staff_details(driver)
                # gram_panch_schema['meetings'] = _meetings(driver)
                # gram_panch_schema['proceedings_'] = proceed(driver)
                gram_panch_schema['rev_collection'] = rev_coll(driver)

                update_clean_list(gram_panch_schema, dist, tal)
                try:
                    handles = driver.window_handles
                    driver.switch_to.window(handles[1])
                    driver.close()
                    driver.switch_to.window((handles[2]))
                    driver.close()
                except:
                    continue


if __name__ == '__main__':
    gp_scraping()
