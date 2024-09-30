import pandas as pd
import json


def excel_to_json(excel_file, json_file):
    # Read the Excel file
    df = pd.read_excel(excel_file, engine='openpyxl')

    # Replace NaN values with empty strings
    df = df.fillna("")

    # Convert DataFrame to JSON (records as list of dictionaries)
    records = df.to_dict(orient='records')

    # Write pretty-printed JSON to file
    with open(json_file, 'w') as f:
        json.dump(records, f, indent=4)

    print(f"Converted {excel_file} to {json_file}")


# Example usage
excel_file = r"D:\translated_file.xlsx" # Replace with your Excel file
json_file = r'D:\output1.json'  # Replace with your desired JSON output file
excel_to_json(excel_file, json_file)