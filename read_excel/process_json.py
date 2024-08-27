import json


# def process_village(village):
#     try:
#         # Ensure names are strings and split by newlines
#         names = str(village.get("Name", "")).strip().split('\n')
#
#         # Convert phone numbers to strings and split by newlines
#         ph_no_raw = village.get("Ph_no", "")
#         phone_numbers = str(ph_no_raw).strip().split('\n')
#
#         # Handle cases where Ph_no might be a single integer
#         if len(phone_numbers) == 1 and phone_numbers[0].isdigit():
#             phone_numbers = [phone_numbers[0]] * len(names)
#
#         # Check if the counts match
#         if len(names) != len(phone_numbers):
#             print(
#                 f"Warning: Mismatch in names and phone numbers count for village: {village.get('village_name', 'Unknown')}")
#             print(f"Names: {names}")
#             print(f"Phone Numbers: {phone_numbers}")
#             return None  # Return None to indicate an issue
#
#         # Create a dictionary with names as keys and phone numbers as values
#         village_data = {}
#         for name, phone in zip(names, phone_numbers):
#             village_data[name.strip()] = phone.strip()
#
#         return village_data
#
#     except AttributeError as e:
#         print(f"Error processing village data: {e}")
#         print(f"Village data: {village}")
#         return None
#
#
# def read_and_process_json(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     all_villages = [process_village(village) for village in data]
#
#     # Filter out None results (where there was a mismatch or error)
#     return [village for village in all_villages if village is not None]
#
#
# # Specify the path to your JSON file
# file_path = fr"C:\Users\HP\Downloads\villagewise_list (2).json"  # Replace with the actual path to your JSON file
#
# # Process the JSON file
# try:
#     all_villages = read_and_process_json(file_path)
#
#     # Print results
#     for village_data in all_villages:
#         if village_data:  # Only print non-empty results
#             print("Village Data:")
#             for name, phone in village_data.items():
#                 print(f"Name: {name}, Phone: {phone}")
#             print("\n")
#
# except FileNotFoundError:
#     print(f"Error: The file at path '{file_path}' was not found.")
# except json.JSONDecodeError:
#     print("Error: Failed to decode JSON. Please check the file format.")
# except ValueError as ve:
#     print(f"Error: {ve}")
# except Exception as e:
#     print(f"Unexpected error: {e}")

##########################################################################################

import json
import os


def process_village(village):
    try:
        # Extract other details
        village_details = {
            "No": village.get("No"),
            "gp_name": village.get("gp_name"),
            "village_serial_no": village.get("village_serial_no"),
            "village_name": village.get("village_name")
        }

        # Extract names and phone numbers, handle missing or invalid data
        names_raw = village.get("Name", "")
        ph_no_raw = village.get("Ph_no", "")

        # Debugging information
        print(f"Processing village: {village.get('village_name', 'Unknown')}")
        print(f"Raw names: {names_raw}")
        print(f"Raw phone numbers: {ph_no_raw}")

        if isinstance(names_raw, str):
            names = names_raw.strip().split('\n')
        else:
            print(f"Warning: 'Name' field is not a string in village: {village.get('village_name', 'Unknown')}")
            names = []

        if isinstance(ph_no_raw, str):
            phone_numbers = ph_no_raw.strip().split('\n')
        else:
            print(f"Warning: 'Ph_no' field is not a string in village: {village.get('village_name', 'Unknown')}")
            phone_numbers = []

        # Handle cases where phone numbers or names might be missing or mismatched
        if len(phone_numbers) == 1 and len(names) > 1:
            phone_numbers = [phone_numbers[0]] * len(names)
        elif len(names) != len(phone_numbers):
            print(
                f"Warning: Mismatch in names and phone numbers count for village: {village.get('village_name', 'Unknown')}")
            max_len = max(len(names), len(phone_numbers))
            if len(names) < max_len:
                names.extend([''] * (max_len - len(names)))
            if len(phone_numbers) < max_len:
                phone_numbers.extend([''] * (max_len - len(phone_numbers)))

        # Create a list of dictionaries with names and phone numbers
        village_data = []
        for name, phone in zip(names, phone_numbers):
            if name.strip() and phone.strip() and phone.strip() != '++++++++':
                village_data.append({
                    "Name": name.strip(),
                    "Phone": phone.strip()
                })

        # Update the village details with the new data
        updated_village = village_details
        updated_village["Members"] = village_data

        return updated_village

    except Exception as e:
        print(f"Error processing village data: {e}")
        print(f"Village data: {village}")
        return None


def read_and_process_json(file_path):
    try:
        # Check if the file exists and is accessible
        if not os.path.isfile(file_path):
            print(f"Error: The file at path '{file_path}' does not exist.")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Debugging information
        print(f"Loaded JSON data: {data}")

        if not data:
            print("Warning: The loaded JSON data is empty.")

        all_villages = [process_village(village) for village in data]

        # Filter out None results (where there was a mismatch or error)
        valid_villages = [village for village in all_villages if village is not None]

        # Debugging information
        print(f"Valid villages: {valid_villages}")

        return valid_villages

    except FileNotFoundError:
        print(f"Error: The file at path '{file_path}' was not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def write_updated_json(file_path, updated_data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(updated_data, file, indent=4, ensure_ascii=False)
        print(f"Updated JSON data has been written to {file_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")


# Specify the path to your JSON file
file_path = fr"C:\Users\HP\Downloads\villagewise_list (2).json"  # Replace with the actual path to your JSON file

# Process and update the JSON file
try:
    updated_villages = read_and_process_json(file_path)

    if not updated_villages:
        print("No valid village data found. Please check the input data.")
    else:
        write_updated_json(file_path, updated_villages)

except Exception as e:
    print(f"Unexpected error: {e}")


