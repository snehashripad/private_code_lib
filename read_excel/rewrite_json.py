import json


def update_ids_in_json(input_file, output_file):
    """
    Reads a JSON file, updates the 'id' values sequentially, and writes the updated data to a new file.

    Parameters:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file with updated IDs.
    """
    # Load the JSON data from the input file with UTF-8 encoding
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Update the 'id' values
    for index, item in enumerate(data):
        item['id'] = index + 1

    # Write the updated JSON data to the output file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("ID values have been updated successfully.")


# Example usage
input_file_path = r"D:\Influencer_master_data.json"
output_file_path = r'D:\updated_influencer_master_data.json'
update_ids_in_json(input_file_path, output_file_path)
