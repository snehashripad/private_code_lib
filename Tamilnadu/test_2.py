import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://localbodydata.com/gram-panchayat-pallur-232657"

# Send a request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the webpage content
    soup = BeautifulSoup(response.content, 'html.parser')


    # Function to extract table data
    def extract_table(table):
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = row.find_all(['td', 'th'])
            cells = [cell.text.strip() for cell in cells]
            rows.append(cells)
        return headers, rows


    # Extracting Address
    address_section = soup.find('section', {'id': 'Address'})
    address = {}
    if address_section:
        address['Panchayat Office'] = address_section.find_all('td')[0].text.strip()
        address['Pincode'] = address_section.find_all('td')[2].text.strip()
        address['Email'] = address_section.find_all('td')[4].text.strip()

    # Extracting Sarpanch
    sarpanch_section = soup.find('section', {'id': 'Sarpanch'})
    sarpanch = {}
    if sarpanch_section:
        sarpanch['Name'] = sarpanch_section.find_all('td')[0].text.strip()
        sarpanch['Mobile No'] = sarpanch_section.find_all('td')[2].text.strip()

    # Extracting Secretary
    secretary_section = soup.find('section', {'id': 'Secretary'})
    secretary = {}
    if secretary_section:
        secretary['Name'] = secretary_section.find_all('td')[0].text.strip()
        secretary['Mobile No'] = secretary_section.find_all('td')[2].text.strip()
        secretary['Email'] = secretary_section.find_all('td')[4].text.strip()

    # Extracting Wards
    wards_section = soup.find('section', {'id': 'Wards'})
    if wards_section:
        ward_table = wards_section.find('table')
        ward_headers, ward_rows = extract_table(ward_table)

    # Extracting Members
    members_section = soup.find('section', {'id': 'Members'})
    if members_section:
        member_table = members_section.find('table')
        member_headers, member_rows = extract_table(member_table)

    # Extracting Schools
    schools_section = soup.find('section', {'id': 'Schools'})
    if schools_section:
        school_table = schools_section.find('table')
        school_headers, school_rows = extract_table(school_table)

    # Printing extracted data
    print("Address:", address)
    print("\nSarpanch:", sarpanch)
    print("\nSecretary:", secretary)
    print("\nWards:")
    print(ward_headers)
    for row in ward_rows:
        print(row)
    print("\nMembers:")
    print(member_headers)
    for row in member_rows:
        print(row)
    print("\nSchools:")
    print(school_headers)
    for row in school_rows:
        print(row)
else:
    print("Failed to retrieve the webpage")

