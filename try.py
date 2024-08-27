from time import sleep
import srsly
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

clean_list = []


def update_com_list(gp_schema):
    clean_list.append(gp_schema)
    srsly.write_json(rf'D:\Tamilnadu\pallur.json', clean_list)


def gp_links(driver):
    gp_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links = [x.get_attribute('href').strip() for x in gp_links]
    all_gp_data = {}
    for link in links[1::2]:
        # r_link = links[62]
        driver.get(link)
        container = driver.find_element(By.CSS_SELECTOR, '.container')
        rows = container.find_elements(By.CSS_SELECTOR, 'div.row')
        for row in rows:
            headings = row.find_elements(By.CSS_SELECTOR, 'h2')
            if len(headings) == 0:
                continue
            print(headings[0].text())


        exit(0)

def PC_details():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(rf"https://localbodydata.com/parliamentary-constituencies-list-in-tamil-nadu-state-33")
    sleep(5)
    driver.maximize_window()
    pc_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')

    links = [x.get_attribute('href').strip() for x in pc_links]
    # links = set(links)
    unique_links = []

    for link in links:
        if link not in unique_links:
            unique_links.append(link)
    first_link = unique_links[0]

# for link in unique_links:
    driver.get(first_link)

    ac_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr/td/a')
    links_ = [x.get_attribute('href').strip() for x in ac_links]
    # links_ = set(links_)
    for link in links_:
        driver.get(link)
        sleep(2)

        table_rows = driver.find_elements(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr')
        count = len(table_rows)
        sleep(1)
        complete_list = []
        for i in range(1, count + 1):
            dict_village_details = {}
            dict_village_details['Sl.no'] = \
                driver.find_elements(By.XPATH,
                                     f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[1]')[
                    0].text
            dict_village_details[' Village_name'] = driver.find_elements(By.XPATH,
                                                                         f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[2]')[
                0].text
            dict_village_details['Gram_panchayat_name'] = driver.find_elements(By.XPATH,
                                                                               f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[3]')[
                0].text
            dict_village_details['Sub_dristrict_name'] = driver.find_elements(By.XPATH,
                                                                              f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[4]')[
                0].text
            dict_village_details['District_name'] = driver.find_elements(By.XPATH,
                                                                         f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[5]')[
                0].text
            dict_village_details['AC_name'] = driver.find_elements(By.XPATH,
                                                                   f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[6]')[
                0].text
            dict_village_details['PC_name'] = driver.find_elements(By.XPATH,
                                                                   f'/html/body/div[3]/div[1]/div/div/div/div/table/tbody/tr[{i}]/td[7]')[
                0].text

            complete_list.append(dict_village_details)
            gp_schema = {'GP_details': dict_village_details, 'gp_mem' : gp_links(driver)}
            update_com_list(gp_schema)


if __name__ == '__main__':
    PC_details()
