import json
from fuzzywuzzy import fuzz
from sample import write_json


def merge_json():
    try:
        # Load JSON data
        with open(r"D:\excel_to_json\data_injection\KPCC.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        with open(r"C:\Users\HP\Downloads\mulbagal_hierarchy.json", "r", encoding="utf-8") as f:
            data1 = json.load(f)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Extract 'children' from data1
    da = [x.get('children', []) for x in data1]

    # Flatten the list of children
    flat_da = [item for sublist in da for item in sublist]

    # Prepare to store matches
    matches = []

    # Iterate through both datasets
    for data_item in data:
        village = data_item.get('Village', '')
        if not village:
            continue  # Skip items without a 'Village' key

        for da1_item in flat_da:
            village1 = da1_item.get('village_name', '')
            if not village1:
                continue  # Skip items without a 'village_name' key

            # Perform fuzzy matching
            ratio = fuzz.ratio(village.lower(), village1.lower())

            if ratio >= 85:
                data_item.update({'node': da1_item})
                matches.append((village, village1, ratio))

    # Save the updated data to the JSON file
    try:
        write_json(data, r'D:\excel_to_json\data_injection\KPCC1_node_match.json')
    except Exception as e:
        print(f"Error writing JSON: {e}")
        return

    # Output the results
    for match in matches:
        print(f"Match found: {match[0]} <-> {match[1]} with ratio {match[2]}")


# Ensure the function is called
if __name__ == "__main__":
    merge_json()
