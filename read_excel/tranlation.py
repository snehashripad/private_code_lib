import pandas as pd
from googletrans import Translator

# Initialize translator
translator = Translator()

# Function to translate text
def translate_text(text, src='kn', dest='en'):
    try:
        translated = translator.translate(text, src=src, dest=dest)
        return translated.text
    except Exception as e:
        print(f"Error: {e}")
        return text

# Load the Excel file
df = pd.read_excel(rf"D:\excel_to_json1.xlsx", engine='openpyxl')

# Translate the specified column
def translate_column(column):
    return column.apply(lambda x: translate_text(x) if isinstance(x, str) else x)

# Assuming the Kannada text is in a column named 'KannadaText'
df['Englishname'] = translate_column(df['village_name'])

# Save the updated DataFrame to a new Excel file
df.to_excel(rf'D:\translated_file_village.xlsx', index=False, engine='openpyxl')
