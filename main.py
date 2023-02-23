import random
from data_analysis import *

import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

iter = 0
content = []
list_col_names = ['index', 'Data', 'Zamknięcie', 'Otwarcie', 'Max', 'Min']
open_, max_, min_ = "", "", ""
url = "https://pl.investing.com/crypto/bitcoin/historical-data"
request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(request_site).read()
a = BeautifulSoup(webpage, 'html.parser')
rows = a.find_all('tr')
df_temp = pd.Series(np.arange(31, -1, -1, dtype=int))  # Reversed index column


def regex(df, col_name, what_to_replace, replacer, regex_bool):
    df[col_name] = df[col_name].str.replace(what_to_replace, replacer, regex=regex_bool)


def rename_df_cols(df, list):
    df.columns = list


def col_to_type(df, name, type):
    df[name] = df[name].astype(type)


def df_to_type(df, list):
    for i in range(0, len(list)):
        reg_list = re.findall("[0-9]+", str(df[list[i]].values[0]))
        if i < 1:
            col_to_type(df, list[i], int)
        elif not (len(reg_list[0]) == 2 and len(reg_list[1]) == 2):  # without 'date', date regex validation
            col_to_type(df, list[i], float)


for result in rows:
    ind = 0
    cells = result.find_all(['td', 'th'])
    for cell in cells:
        ind = ind + 1
        string = re.findall("[0-9]+", str(cell.attrs))
        if string and len(string) > 2:
            string = string[0] + string[1] + "." + string[2]

        match ind:
            case 3:
                open_ = string
            case 4:
                max_ = string
            case 5:
                min_ = string

    date = result.find('td', class_='first left bold noWrap')
    if result.find('td', class_='greenFont') is not None:
        cena = result.find('td', class_='greenFont')
    else:
        cena = result.find('td', class_='redFont')
    if date is not None and cena is not None:
        date_ = date.text
        content.append([date_, cena.text, open_, max_, min_])

content_df = pd.DataFrame(content)  # DF Load
content_df = content_df.reset_index()  # Index as new column
content_df['index'] = df_temp  # Assigning temp reversed index column as main callable index column

#   Data managing, types changes and regexes

rename_df_cols(content_df, ['index', 'Data', 'Zamknięcie', 'Otwarcie', 'Max', 'Min'])
regex(content_df, 'Zamknięcie', '.', '', True)
regex(content_df, 'Zamknięcie', ',', '.', False)
df_to_type(content_df, list_col_names)
content_df = content_df.iloc[::-1]  # Sorting main scrapped data, index order dependent

