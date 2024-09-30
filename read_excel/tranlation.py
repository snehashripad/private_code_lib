import pandas as pd
from googletrans import Translator

translator = Translator()

def translate_text(text, src='kn', dest='en'):
    try:
        translated = translator.translate(text, src=src, dest=dest)
        return translated.text
    except Exception as e:
        print(f"Error: {e}")
        return text


df = pd.read_excel(rf"D:\excel_to_json1.xlsx", engine='openpyxl')


def translate_column(column):
    return column.apply(lambda x: translate_text(x) if isinstance(x, str) else x)


df['Englishname'] = translate_column(df['village_name'])

df.to_excel(rf'D:\translated_file_village.xlsx', index=False, engine='openpyxl')
