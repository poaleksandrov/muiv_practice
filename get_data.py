from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import re
import time
from googletrans import Translator

# Создание экземпляра переводчика
translator = Translator()

# Список интересующих тем и их переводы
categories = [
    'sci.crypt',
    'sci.electronics',
    'sci.med',
    'sci.space',
    'soc.religion.christian'
]

# Словарь для перевода категорий
category_translations = {
    'sci.crypt': 'криптография',
    'sci.electronics': 'электроника',
    'sci.med': 'медицина',
    'sci.space': 'космос',
    'soc.religion.christian': 'христианство'
}

# Загрузка данных только по выбранным категориям
newsgroups_selected = fetch_20newsgroups(subset='all', categories=categories, shuffle=True, random_state=42)

# Функция для очистки текста
def clean_text(text):
    # Удаление заголовков и метаданных
    text = re.sub(r'^Subject:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^From:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Reply-To:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^In-Reply-To:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Lines:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Keywords:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Message-ID:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^NNTP-Posting-Host:.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[A-Za-z\-]+:.*\n?', '', text, flags=re.MULTILINE)
    
    # Удаление подписей и нижних колонтитулов
    text = re.sub(r'-- \n.*', '', text, flags=re.MULTILINE)
    
    # Удаление цифр
    text = re.sub(r'\d+', '', text)
    
    # Удаление email-адресов и символов "@"
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'@\S+', '', text)
    
    # Удаление лишних пробелов и переводов строк
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Функция для перевода текста
def translate_text(text):
    try:
        translated = translator.translate(text, src='en', dest='ru')
        return translated.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # Возвращаем исходный текст в случае ошибки

# Очистка текстов и перевод
cleaned_texts = [clean_text(text) for text in newsgroups_selected.data]
translated_texts = []

for text in cleaned_texts:
    translated_text = translate_text(text)
    translated_texts.append(translated_text)
    time.sleep(1)  # Добавляем задержку, чтобы избежать превышения лимита запросов к API

# Перевод категорий
translated_categories = [category_translations[newsgroups_selected.target_names[target]] for target in newsgroups_selected.target]

# Создание DataFrame
df_selected = pd.DataFrame({'text': translated_texts, 'topic': translated_categories})

# Сохранение в CSV файл
df_selected.to_csv('20newsgroups_selected_cleaned_translated.csv', index=False)

# Вывод первых 5 строк для проверки
print(df_selected.head())
