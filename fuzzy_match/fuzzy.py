import glob
from shutil import copy

import srsly
from fuzzywuzzy.process import extractOne

import json
import os
import re
from fuzzywuzzy import fuzz

def normalize_text(text):
    if isinstance(text, str):
        text = text.lower().strip()  # Convert to lowercase and strip whitespace
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

def merge_json(single_json_file, folder_path, prefix=""):
    # Load the single JSON file
    try:
        with open(single_json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    # Extract the list from the 'flat_list' key
    single_data = json_data.get('flat_list', [])

    if not isinstance(single_data, list):
        print("Expected the 'flat_list' key to contain a list of dictionaries.")
        return

    # Get filenames from the folder
    try:
        filenames = [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith('.json')]
    except Exception as e:
        print(f"Error listing files in folder: {e}")
        return

    # Normalize filenames
    filenames = [normalize_text(filename) for filename in filenames]

    # Prepare to store matches
    matches = []
    filename_replacements = {}  # Dictionary to store filename replacements

    # Iterate through the single JSON data and match with filenames
    for data_item in single_data:
        if isinstance(data_item, dict):
            key_value = data_item.get('name1', '')
            replacement_value = data_item.get('ac3', '')

            # Normalize the key_value
            key_value = normalize_text(key_value)

            # Perform matching
            for filename_ in filenames:
                filename = filename_.split()[5:-1]
                filename = ' '.join(filename)
                ratio = fuzz.ratio(key_value.lower(), filename.lower())

                # Print comparison details for debugging
                #print(f"Comparing '{key_value}' with filename '{filename}' - Ratio: {ratio}")

                # Adjust the threshold as needed
                if ratio >= 90:  # Threshold set to 60
                    # Record the filename replacement
                    old_filename = os.path.join(folder_path, f"{filename_}.json")
                    new_filename = os.path.join(folder_path, f"{prefix}{normalize_text(replacement_value)}.json")
                    print(fr'{key_value} -> {filename}')
                    '''
                    # Print details of replacement for debugging
                    print(f"Match found: '{key_value}' -> '{filename}' with Ratio: {ratio}")
                    print(f"Old Filename: '{old_filename}'")
                    print(f"New Filename: '{new_filename}'")
    
                    filename_replacements[old_filename] = new_filename
                    data_item.update({'filename_match': filename})
                    matches.append((key_value, filename, ratio, replacement_value))
                    '''
    # # Save the updated single JSON data
    # try:
    #     with open(single_json_file, "w", encoding="utf-8") as f:
    #         json.dump(json_data, f, ensure_ascii=False, indent=4)
    # except Exception as e:
    #     print(f"Error saving JSON file: {e}")
    #     return

    # Print the matches
    if matches:
        print("Matches found:")
        for match in matches:
            print(f"Value: '{match[0]}' matched with Filename: '{match[1]}' with Ratio: {match[2]} and Replacement: '{match[3]}'")
    else:
        print("No matches found.")

    # Rename the files
    print("Attempting to rename files...")
    for old_filename, new_filename in filename_replacements.items():
        if os.path.exists(old_filename):
            # Ensure new filename doesn't already exist to avoid overwriting
            if not os.path.exists(new_filename):
                try:
                    os.rename(old_filename, new_filename)
                    print(f"Renamed '{old_filename}' to '{new_filename}'")
                except Exception as e:
                    print(f"Error renaming '{old_filename}' to '{new_filename}': {e}")
            else:
                print(f"Cannot rename '{old_filename}' to '{new_filename}' because the target file already exists.")
        else:
            print(f"File '{old_filename}' does not exist.")

def old():
    # Example usage
    single_json_file = r"C:\Users\HP\Downloads\ac_list_prep.json"
    folder_path = r"D:\new"
    prefix = "ac_"
    merge_json(single_json_file, folder_path, prefix)


def clean_file(file):
    file = os.path.basename(file).strip()\
        .replace('.json','')\
        .replace('Gram Panchayats List In Assembly','')
    file = [x.strip() for x in file.split(' ') if x.strip().replace('.','').isalpha()]
    return ' '.join(file).strip()




if __name__ == '__main__':
    files = glob.glob(fr'D:\data_extrac_dupli\*.json')
    acs_to_match = [clean_file(x) for x in files]
    acs_master = srsly.read_json(r"C:\Users\HP\Downloads\ac_list_prep.json")
    match_target = list(acs_master['acname_ac_dict'].keys())

    for idx in range(len(files)):
        src = acs_to_match[idx]
        match = extractOne(src, match_target)
        ac_obj = acs_master['acname_ac_dict'][match[0]]
        ac3 = ac_obj['ac3']

        dest  =fr'D:\ac_mapped\ac_{ac3}.json'
        copy(files[idx], dest)
        print(fr'{files[idx]} -> {ac3}')
