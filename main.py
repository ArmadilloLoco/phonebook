import re
import numpy as np
import pandas as pd


def phone_format(phone: str) -> str:
    ''' Функция для форматирования номера телефона '''
    clean = re.sub(r'[^0-9\w\.]', '', phone)
    pattern = r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(доб\.\d+|)'
    formatted = re.sub(pattern, r'\1(\2)\3-\4-\5 \6', '+7' + clean[1:]).strip()
    return formatted

if __name__ == '__main__':
    df = pd.read_csv('phonebook_raw.csv', encoding='utf-8') # чтение csv

    # Разделение ФИО на lastname, firstname, surname
    full_names = df['lastname'].str.split(expand=True)
    df['lastname'] = full_names[0]
    df['firstname'] = full_names[1].fillna(df['firstname'])
    df['surname'] = full_names[2].fillna(df['firstname'].str.split().str[1]).fillna(df['surname'])
    df_merge = df.groupby(['lastname','firstname','surname']).agg(lambda x: x.dropna().iloc[0] 
                                                                  if x.dropna().any()
                                                                  else np.nan
                                                                  ).reset_index() # объединение дублирующихся записей
    df_merge['phone'] = (df_merge['phone'].apply(phone_format)) # форматирование номера телефона
    df_merge.to_csv('phonebook_clean.csv', encoding='utf-8', index=False) # запись в csv