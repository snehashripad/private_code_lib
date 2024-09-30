import os


def create_folders(folder_names, base_directory="D:\Tamilnadu\PC\Arani"):
    for folder_name in folder_names:
        directory = os.path.join(base_directory, folder_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Folder '{folder_name}' created successfully.")
        else:
            print(f"Folder '{folder_name}' already exists.")


# Example usage
folders_to_create = ["Kancheepuram", 'Kanniyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai',
                     'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pollachi', 'Ramanathapuram', 'Salem', 'Sivaganga', 'Sriperumbudur', 'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukkudi', 'Tiruchirappalli', 'Tirunelveli', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Vellore', 'Viluppuram', 'Virudhunagar']
create_folders(folders_to_create, "D:\Tamilnadu\PC")
