import json


def update_json_file(input_file_path, output_file_path):

    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
        return
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return

    # Update JSON data
    for item in data:
        # Move 'village' key to 'more' dictionary
        if 'Village' in item:
            item['more']['Village'] = item.pop('Village')

        # Ensure 'node' key exists
        if 'node' not in item:
            item['node'] = {}

    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print("JSON file has been updated and saved.")
    except UnicodeEncodeError as e:
        print(f"UnicodeEncodeError: {e}")
    except IOError as e:
        print(f"IOError: {e}")


# Example usage
# File paths
input_file_path = r"D:\excel_to_json\data_injection\kpcc.json"
output_file_path = r'D:\excel_to_json\data_injection\updated\kpcc.json'
update_json_file(input_file_path, output_file_path)
