import time
import asyncio


def await_time_limit(time_limit):
    def inner(func):
        async def wrapper(*args, **kwargs):
            return await asyncio.wait_for(func(*args, **kwargs), time_limit)
        return wrapper
    return inner
# download_pdf(article_schema['PDF_LINk'], f"{folder_path}/{article_schema['Journal_Details']}-{index}.pdf")



import os,glob

def get_last_filename_and_rename(save_folder, new_filename):
    files = glob.glob(save_folder + '/*')
    max_file = max(files, key=os.path.getctime)
    filename = max_file.split("/")[-1].split(".")[0]
    new_path = max_file.replace(filename, new_filename)
    os.rename(max_file, new_path)
    return new_path

dest_filename = f"D:\data"
def download_pdf(link_, dest_filename):
    if file_exists(dest_filename):
        return link_

    incomplete = dest_filename + '.pdf'
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        r = requests.get(link_, headers)
        if r.status_code == requests.codes.ok:
            with open(incomplete, 'wb') as f:
                for data in r:
                    f.write(data)
        os.rename(incomplete, dest_filename)
        # get_pdf_link(driver)
    except Exception as e2:
        return None


def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def create_new_folder(article_shcema):
    get_all_links(driver)
    folder_path = rf"D:\data\{article_shcema['year']}"
    ensure_dir(folder_path)
    print(folder_path)
    return folder_path

