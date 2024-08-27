import os

source_folder = r"C:\temp\data"f

for item in os.listdir(source_folder):
    if os.path.isfile(os.path.join(source_folder, item)):
        if item.endswith(".pdf"):
            try:
                os.rename(os.path.join(source_folder, item), os.path.join(source_folder, '2023_journal' + item))
            except PermissionError:
                continue
            except Exception as e:
                raise Exception('e')