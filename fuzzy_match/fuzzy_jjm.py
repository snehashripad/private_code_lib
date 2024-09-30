import os
import glob
import shutil
import json
from fuzzywuzzy import process


def clean_file(file):
    file = os.path.basename(file).strip() \
        .replace('.json', '')
    file = [x.strip() for x in file.split(' ') if x.strip().replace('.', '').isalpha()]
    return ' '.join(file).strip()


def load_master_json(master_json_path):
    with open(master_json_path, 'r') as file:
        return json.load(file)


def process_files(files, master_data, output_dir):
    ac_name_to_ac3 = {}
    for entry in master_data['acname_ac_dict'].values():
        ac_names = [entry.get('name1'), entry.get('name2')]
        ac3 = entry.get('ac3')
        for ac_name in ac_names:
            if ac_name:
                ac_name_to_ac3[ac_name] = ac3

    print("AC Name to AC3 Mapping:", ac_name_to_ac3)

    for file_path in files:
        src_name = clean_file(file_path)
        taluk_name = src_name

        print(f"Processing file: {file_path}")
        print(f"Cleaned file name: {src_name}")

        match = process.extractOne(taluk_name, ac_name_to_ac3.keys())

        if match:
            matched_name, score = match
            print(f"Fuzzy Match: {matched_name} with score {score}")
            if score > 80:
                ac3 = ac_name_to_ac3[matched_name]
                dest_folder = os.path.join(output_dir, f'ac_{ac3}')
                os.makedirs(dest_folder, exist_ok=True)

                dest_file_path = os.path.join(dest_folder, os.path.basename(file_path))
                shutil.copy(file_path, dest_file_path)
                print(f'{file_path} -> {dest_file_path}')
            else:
                print(f'No good match found for: {file_path} (Score: {score})')
        else:
            print(f'No match found for: {file_path}')


if __name__ == '__main__':
    master_json_path = r"C:\Users\HP\Downloads\ac_list_prep.json"
    files_folder = r'D:\jjm\extracted_data\Ahmednagar_data'
    output_folder = r'D:\jjm\ac_mapped'

    files = glob.glob(os.path.join(files_folder, '*.json'))
    master_data = load_master_json(master_json_path)

    process_files(files, master_data, output_folder)
