import json
import pandas as pd

def read_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def convert_json_to_dataframe(json_data):
    """Convert JSON data to a pandas DataFrame."""
    # Normalize JSON data to handle nested structures
    df = pd.json_normalize(json_data)
    return df

def write_dataframe_to_excel(dataframe, output_filepath):
    try:
        dataframe.to_excel(output_filepath, index=False, engine='openpyxl')
        print(f"Successfully wrote Excel file to {output_filepath}")
    except Exception as e:
        print(f"Error writing Excel file to {output_filepath}: {e}")

if __name__ == '__main__':
    # Filepath for JSON data
    json_filepath = r"C:\Users\HP\Downloads\updated_villagewise_list.json"  # Replace with the path to your JSON file

    # Read the JSON data
    json_data = read_json(json_filepath)

    # Convert JSON data to DataFrame
    df = convert_json_to_dataframe(json_data)

    # Filepath for the output Excel file
    excel_filepath = r'D:\excel_to_json1.xlsx'  # Replace with the desired output file path

    # Write DataFrame to Excel
    write_dataframe_to_excel(df, excel_filepath)
