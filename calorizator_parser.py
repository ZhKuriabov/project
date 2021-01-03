import requests
import csv
import pandas as pd

df_list = []
for i in range(74):
    URL = 'https://calorizator.ru/product/all?page=' + f'{i}'
    r = requests.get(URL)
    print(i)
    df_list.append(pd.read_html(r.text)[0])

df = pd.concat(df_list)

del df['Unnamed: 0']
# df.to_csv('calorizator.csv', index=False)