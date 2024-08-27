import glob
from time import sleep
import srsly
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

com_list = {}


def update_com_list(vp_schema):
    com_list = {}
    srsly.write_json(rf'D:\temp.json', com_list)


def vil_level_committe(driver):
    rows = driver.find_elements(By.XPATH, '//*[@id="CPHPage_divgrid"]/div/div[7]/div[2]/div[2]/div[2]/table/tbody/tr')
    count = len(rows)
    sleep(1)
    cont_list = []


# Village level functionaries contacts
def vil_level_fun_contacts(driver):
    rows = driver.find_elements(By.XPATH, '//*[@id="CPHPage_divgrid"]/div/div[7]/div[2]/div[1]/div[2]/table/tbody/tr')
    count = len(rows)
    sleep(1)
    contact_list = []
    for i in range(1, count + 1):
        dict_gp_contacts = {}
        dict_gp_contacts['sl.no'] = driver.find_elements(By.XPATH,
                                                         f'//*[@id="CPHPage_divgrid"]/div/div[7]/div[2]/div[1]/div[2]/table/tbody/tr[{i}]/td[1]')[
            0].text
        dict_gp_contacts['name'] = driver.find_elements(By.XPATH,
                                                        f'//*[@id="CPHPage_divgrid"]/div/div[7]/div[2]/div[1]/div[2]/table/tbody/tr[{i}]/td[2]')[
            0].text
        dict_gp_contacts['designation'] = driver.find_elements(By.XPATH,
                                                               f'//*[@id="CPHPage_divgrid"]/div/div[7]/div[2]/div[1]/div[2]/table/tbody/tr[{i}]/td[3]')[
            0].text
        dict_gp_contacts['phone'] = driver.find_elements(By.XPATH,
                                                         f'//*[@id="CPHPage_divgrid"]/div/div[7]/div[2]/div[1]/div[2]/table/tbody/tr[{i}]/td[5]')[
            0].text

        sleep(1)
        contact_list.append(dict_gp_contacts)

    return contact_list


def hab_list(driver):
    rows = driver.find_elements(By.XPATH, '//*[@id="CPHPage_div_Hablist"]/div/div/table/tbody/tr')
    count = len(rows)
    sleep(1)
    habitation_list = []
    for i in range(1, count + 1):
        dict_habitation_list = {}
        dict_habitation_list['sl.no'] = \
            driver.find_elements(By.XPATH, f'//*[@id="CPHPage_div_Hablist"]/div/div/table/tbody/tr[{i}]/td[1]')[0].text
        dict_habitation_list['Habitation_name'] = \
            driver.find_elements(By.XPATH, f'//*[@id="CPHPage_div_Hablist"]/div/div/table/tbody/tr[{i}]/td[2]')[0].text
        dict_habitation_list['total_population'] = \
            driver.find_elements(By.XPATH, f'//*[@id="CPHPage_div_Hablist"]/div/div/table/tbody/tr[{i}]/td[3]')[0].text
        dict_habitation_list['SC_population'] = \
            driver.find_elements(By.XPATH, f'//*[@id="CPHPage_div_Hablist"]/div/div/table/tbody/tr[{i}]/td[4]')[0].text
        dict_habitation_list['ST_population'] = \
            driver.find_elements(By.XPATH, f'//*[@id="CPHPage_div_Hablist"]/div/div/table/tbody/tr[{i}]/td[5]')[0].text
        dict_habitation_list['GEN_population'] = \
            driver.find_elements(By.XPATH, f'//*[@id="CPHPage_div_Hablist"]/div/div/table/tbody/tr[{i}]/td[6]')[0].text
        habitation_list.append(dict_habitation_list)

    return habitation_list


def html_scrape():
    options = FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    # html_files = glob.glob(rf"D:/jjm/Maharashtra/*/*/*/*/*.html")
    #
    # for html in html_files:
    #     html
    driver.get(rf"file:///D:/jjm/Maharashtra/Jalna/Ambad/Alamgaon/Alamgaon/Alamgaon.html")
    sleep(1)
    driver.maximize_window()
    comp_list = []

    dict_village = {}
    dict_village['state'] = driver.find_elements(By.XPATH, '//*[@id="CPHPage_lblState"]')[0].text
    dict_village['district'] = driver.find_elements(By.XPATH, '//*[@id="CPHPage_lblDistrict"]')[0].text
    dict_village['block'] = driver.find_elements(By.XPATH, '//*[@id="CPHPage_lblBlock"]')[0].text
    dict_village['panchayt'] = driver.find_elements(By.XPATH, '//*[@id="CPHPage_lblPanchayat"]')[0].text
    dict_village['village'] = driver.find_elements(By.XPATH, '//*[@id="CPHPage_lblVillage"]')[0].text
    dict_village['no_of_habbitations'] = driver.find_elements(By.XPATH, '//*[@id="CPHPage_lblHab"]')[0].text
    dict_village['habitation_list'] = hab_list(driver)
    dict_village['GP_mem'] = vil_level_fun_contacts(driver)
    comp_list.append(dict_village)

    vp_schema = {'village_details': comp_list}
    update_com_list(vp_schema)


if __name__ == '__main__':
    html_scrape()
