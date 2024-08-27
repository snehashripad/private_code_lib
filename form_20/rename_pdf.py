import os
import shutil

base_folder = "de-ac-bank"
source_path = r"D:\form_20\Haryana\Vidhansabha\2019"
year = "2019"
pdf_type = "Assembly"
# pdf_type = "Parliament"

pdfs = os.listdir(source_path)
for pdf in pdfs:
    ac_no = int(pdf.split(".")[0])

    name = fr"ac_{str(ac_no).zfill(3)}_f20_{year}_{pdf_type}.pdf"

    os.makedirs(fr"D:\form_20\banks\{base_folder}\ac_{str(ac_no).zfill(3)}\ha", exist_ok=True)
    path = fr"D:\form_20\banks\{base_folder}\ac_{str(ac_no).zfill(3)}\ha"

    shutil.copy(fr"{source_path}\{pdf}", fr"{path}\{name}")