import srsly
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

path = r"C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe"
_options = Options()
_options.add_argument("--window-size=1920,1080")

_options.add_experimental_option('detach', True)
service = Service(executable_path=path)


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


def update_clean_list(gram_panch_schema):
    com_list.append(gram_panch_schema)
    srsly.write_json(r'C:\temp\gram_panch.json', com_list)


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
                gram_panch_schema['repre'] = ele_rep_details(driver)
                gram_panch_schema['staff'] = staff_details(driver)
                update_clean_list(gram_panch_schema)
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
# //*[@id="locationFilter_validate__ID"]/div[1]/div/span/span[1]/span
# //*[@id="flt_zp__Id"]/option[2]