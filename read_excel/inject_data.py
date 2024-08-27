
import json

from fuzzywuzzy import fuzz


def json_formater():
    with open(r"C:\Users\HP\Downloads\Teachers_amount_payment.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # with open(r"C:\Users\HP\Downloads\mulbagal_hierarchy (1).json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    # Extracting relevant data
    req_data = [(str(x['Name']), str(x['Mobile']), str(x['Village'])) for x in data]
    # str(x['caste']), str(x['village_name'])
    payload = []

    for i in range(len(req_data)):
        caste_value = req_data[i][2] if req_data[i][2] != "nan" else ""
        # name =
        entry = {
            "id": i+1,
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
            'Village' : req_data[i][2],
            "more": {
                "primary_occupation": "",
                "additional_information": "",
                "local_elections_contested": ""
            },
            "influence": {
                "caste": caste_value,
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

def merge_json():
    import json
    from fuzzywuzzy import fuzz

    # Load JSON data
    with open(r"D:\excel_to_json\data_injection\Teachers_amount_payment.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(r"C:\Users\HP\Downloads\mulbagal_hierarchy (1).json", "r", encoding="utf-8") as f:
        data1 = json.load(f)

    # Extract 'children' from data1
    da = [x['children'] for x in data1]

    # Flatten the list of children (if needed)
    flat_da = [item for sublist in da for item in sublist]

    # Prepare to store matches
    matches = []

    # Iterate through both datasets
    for data_item in data:
        village = data_item.get('Village', '')
        for da1_item in flat_da:
            village1 = da1_item.get('village_name', '')



            # Perform fuzzy matching
            ratio = fuzz.ratio(village, village1)

            if ratio >= 60:
                matches.append((village, village1, ratio))

    # Output the results
    for match in matches:
        print(f"Match found: {match[0]} <-> {match[1]} with ratio {match[2]}")


if __name__ == '__main__':

    filpath = rf"D:\excel_to_json\data_injection\Teachers_amount_payment.json"
    # d = json_formater()
    merge_json()
    def write_json(obj, filepath, ensure_ascii=False):
        try:
            with open(filepath, "w", encoding="utf8", errors='ignore') as f:
                json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)
            print(f"Successfully wrote JSON to {filepath}")
        except Exception as e:
            print(f"Error writing JSON to {filepath}: {e}")
    # write_json(d,filpath)