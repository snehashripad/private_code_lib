import json
import re

def clean_json_content(content):
    # Remove non-JSON characters that are not part of valid JSON
    content = re.sub(r'^[^\[{]*', '', content)  # Remove any leading characters that are not `[`, `{`
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', content)  # Replace control characters

def json_formater():
    filepath = r"D:\output1.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"File content snippet:\n{content[:500]}")  # Print a snippet of the file for inspection
            cleaned_content = clean_json_content(content)
            try:
                data = json.loads(cleaned_content)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Error near position: {e.pos}")
                return []
    except FileNotFoundError:
        print("File not found.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

    # Verify the type and content of data
    if not isinstance(data, list):
        print(f"Data is not a list. Data type: {type(data)}")
        return []

    if len(data) > 0:
        print(f"Data snippet:\n{data[:2]}")

    req_data = [(str(x['Name']), str(x['Ph_no']), str(x['village_name']), str(x['caste'])) for x in data]
    payload = []

    for i in range(len(req_data)):
        entry = {
            "id": i + 1,
            "projectid": 639,
            "profile": {
                "name": req_data[i][0],
                "photo_path": {
                    "path": "",
                    "type": ""
                },
                "phonenumber": req_data[i][1],
                "whatsapp_number": req_data[i][1]
            },
            "village" : req_data[i][2],
            "more": {
                "primary_occupation": "",
                "additional_information": "",
                "local_elections_contested": ""
            },
            "influence": {
                "Caste": req_data[i][3],
                "voters": ""
            },
            "affiliation": {
                "party": "CONGRESS",
                "candidate": "",
                "strength_of_support": ""
            },
            "voter_card_linked": False,
            "voter_card": {},
            "is_volunteer": True,
            "volunteer": {
                "roles": [],
                "position": ""
            },
            "is_app_user": False,
            "userid": 0
        }

        payload.append(entry)
    return payload

if __name__ == '__main__':
    output_filepath = r"D:\excel_to_json\data_injection\vill.json"
    d = json_formater()

    def write_json(obj, filepath, ensure_ascii=False):
        try:
            with open(filepath, "w", encoding="utf8", errors='ignore') as f:
                json.dump(obj, f, indent=4, ensure_ascii=ensure_ascii)
            print(f"Successfully wrote JSON to {filepath}")
        except Exception as e:
            print(f"Error writing JSON to {filepath}: {e}")

    write_json(d, output_filepath)
