import json


def json_div():
    with open(r"C:\Users\TESTING\Downloads\villagewise_list (2).json", "r", encoding="utf-8") as f:
        data = json.load(f)
    name_entries = [x for x in data if '\n' in str(x['Name'])]
    payload = []
    for entry in name_entries:
        _name = entry['Name'].split('\n')

        _ph_no = str(entry['Ph_no']).split('\n')
        _caste = str(entry['caste']).split('\n')
        _addr_no = str(entry['addr_no']).split('\n')
        for name, ph_no,caste,addr_no in zip(_name, _ph_no, _caste, _addr_no):
            new_dict = {
                'No': entry['No'],
                'gp_name': entry['gp_name'],
                'village_serial_no': entry['village_serial_no'],
                'village_name': entry['village_name'],
                'Name': name,
                'Ph_no': ph_no,
                'caste': caste,
                'addr_no': addr_no
            }
            payload.append(new_dict)

    updated_data = [x for x in data if x not in name_entries]
    updated_data.extend(payload)
    with open(r"C:\Users\TESTING\Downloads\updated_villagewise_list.json", "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)