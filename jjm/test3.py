import os
import re
import requests
from bs4 import BeautifulSoup
import json
import time


WORKING_DIR = r'D:\jjm'
STATE_NAME = 'Maharashtra'



def save_html_to_file(html, file_path):
    with open(file_path, 'w', encoding='utf8') as f:
        f.write(html)

def create_directory_if_not_exists(directory):
    directory = re.sub(r'[<>:"/\\|?*]', '', directory)
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_json(obj, filepath, ensure_ascii=False):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf8", errors='ignore') as f:
        json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)


def get_soup(url, params=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        response.raise_for_status()



def get_options_from_select(soup, select_id):
    select_element = soup.find('select', id=select_id)
    options = select_element.find_all('option')[1:]  # Skip the first option if it's a placeholder
    return {option.text.strip(): option['value'] for option in options}

def post_form(url, data):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        response.raise_for_status()



BASE_URL = 'https://ejalshakti.gov.in/JJM/JJM/Public/Profile/VillageProfile.aspx'

def scrape_village_profiles():
    initial_soup = get_soup(BASE_URL)
    states = get_options_from_select(initial_soup, 'CPHPage_ddState')

    for state_name, state_value in states.items():
        if state_name != STATE_NAME:
            continue

        state_dir = os.path.join(WORKING_DIR, state_name)
        create_directory_if_not_exists(state_dir)
        write_json(states, os.path.join(state_dir, 'state.json'))

        state_data = {
            'CPHPage_ddState': state_value,
            '__EVENTTARGET': 'CPHPage_ddState',
            '__EVENTARGUMENT': ''
        }
        state_soup = post_form(BASE_URL, state_data)

        districts = get_options_from_select(state_soup, 'CPHPage_ddDistrict')

        for district_name, district_value in districts.items():
            district_dir = os.path.join(state_dir, district_name)
            create_directory_if_not_exists(district_dir)
            write_json(districts, os.path.join(district_dir, 'district.json'))

            district_data = {
                'CPHPage_ddState': state_value,
                'CPHPage_ddDistrict': district_value,
                '__EVENTTARGET': 'CPHPage_ddDistrict',
                '__EVENTARGUMENT': ''
            }
            district_soup = post_form(BASE_URL, district_data)

            blocks = get_options_from_select(district_soup, 'CPHPage_ddBlock')

            for block_name, block_value in blocks.items():
                block_dir = os.path.join(district_dir, block_name)
                create_directory_if_not_exists(block_dir)
                write_json(blocks, os.path.join(block_dir, 'block.json'))

                block_data = {
                    'CPHPage_ddState': state_value,
                    'CPHPage_ddDistrict': district_value,
                    'CPHPage_ddBlock': block_value,
                    '__EVENTTARGET': 'CPHPage_ddBlock',
                    '__EVENTARGUMENT': ''
                }
                block_soup = post_form(BASE_URL, block_data)

                panchayats = get_options_from_select(block_soup, 'CPHPage_ddPanchayat')

                for panchayat_name, panchayat_value in panchayats.items():
                    panchayat_dir = os.path.join(block_dir, panchayat_name)
                    create_directory_if_not_exists(panchayat_dir)
                    write_json(panchayats, os.path.join(panchayat_dir, 'panchayat.json'))

                    panchayat_data = {
                        'CPHPage_ddState': state_value,
                        'CPHPage_ddDistrict': district_value,
                        'CPHPage_ddBlock': block_value,
                        'CPHPage_ddPanchayat': panchayat_value,
                        '__EVENTTARGET': 'CPHPage_ddPanchayat',
                        '__EVENTARGUMENT': ''
                    }
                    panchayat_soup = post_form(BASE_URL, panchayat_data)

                    villages = get_options_from_select(panchayat_soup, 'CPHPage_ddVillage')

                    for village_name, village_value in villages.items():
                        village_dir = os.path.join(panchayat_dir, village_name)
                        create_directory_if_not_exists(village_dir)
                        write_json(villages, os.path.join(village_dir, 'village.json'))

                        village_data = {
                            'CPHPage_ddState': state_value,
                            'CPHPage_ddDistrict': district_value,
                            'CPHPage_ddBlock': block_value,
                            'CPHPage_ddPanchayat': panchayat_value,
                            'CPHPage_ddVillage': village_value,
                            '__EVENTTARGET': 'CPHPage_ddVillage',
                            '__EVENTARGUMENT': ''
                        }
                        village_soup = post_form(BASE_URL, village_data)

                        show_button = village_soup.find('input', {'id': 'CPHPage_btnShow'})
                        if show_button:
                            village_data['CPHPage_btnShow'] = 'Show'
                            village_soup = post_form(BASE_URL, village_data)

                            habitation_link = village_soup.find('a', {'id': 'CPHPage_lblHab'})
                            if habitation_link:
                                habitation_url = BASE_URL + habitation_link['href']
                                habitation_soup = get_soup(habitation_url)

                                file_name = os.path.join(village_dir, f'{village_name}.html')
                                save_html_to_file(str(habitation_soup), file_name)
                                time.sleep(1)  # To avoid overwhelming the server



if __name__ == '__main__':
    current_dir = fr'{WORKING_DIR}\{STATE_NAME}'
    scrape_village_profiles()
