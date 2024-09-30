import json
import glob

# List of JSON files to merge
file_paths = (r'D:\excel_to_json\data_injection\updated\*.json')  # Adjust the pattern to match your files



def merge_json_files(file_pattern, output_file):

    file_paths = glob.glob(file_pattern)
    merged_data = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    print(f"Warning: File '{file_path}' contains a JSON object. Converting to list.")
                    merged_data.append(data)
                elif isinstance(data, list):
                    merged_data.extend(data)
                else:
                    print(f"Warning: File '{file_path}' contains neither a JSON object nor a list.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file '{file_path}': {e}")
        except Exception as e:
            print(f"An error occurred with file '{file_path}': {e}")

    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(merged_data, f_out, ensure_ascii=False, indent=4)


merge_json_files(file_paths, 'D:\Influencer_master_data.json')
