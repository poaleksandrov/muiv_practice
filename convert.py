import pandas as pd

# Загрузите файл
file_path = '20newsgroups_selected_cleaned_translated.csv'

# Прочитайте файл с правильной кодировкой
df = pd.read_csv(file_path, encoding='utf-8')

# Функция для замены некодируемых символов
def safe_encode(text):
    if isinstance(text, str):
        return text.encode('cp1251', errors='replace').decode('cp1251')
    return text

# Замена символов в столбцах
df['text'] = df['text'].apply(safe_encode)
df['topic'] = df['topic'].apply(safe_encode)

# Сохраните файл в нужной кодировке
output_file_path = 'dataset.csv'
df.to_csv(output_file_path, index=False, encoding='cp1251')

print("Файл успешно сохранен в кодировке cp1251")
