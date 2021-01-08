# This Python file uses the following encoding: utf-8
import os, sys
import pandas as pd
import psycopg2

ingredients = pd.read_csv('ingredients.csv')
full_information = pd.read_csv('full_information.csv')

dirty = []
for i in range(len(full_information['Ingredients'])):
    if 'Title' in full_information['Ingredients'][i]:
        for j in range(len(full_information['Ingredients'][i].split())):
            t = full_information['Ingredients'][i].split()

            if full_information['Ingredients'][i].split()[j] == "{'Title':" or full_information['Ingredients'][i].split()[j] == "[{'Title':":
                dirty.append(t[j] + ' ' + t[j + 1] + ' ' + t[j + 2])
clean = []
for line in dirty:
    # line = line[2:]
    line = line[line.find(":") + 1:]
    line = line[2:]
    line = line[0:line.find("'")]
    if line == 'Для соус':
        line = 'Для соуса'
    clean.append(line)
    # print(line)
clean_unique = list(set(clean))

for i in range(len(ingredients['Name'])):
    for name in range(len(clean_unique)):
        if ingredients['Name'][i] == clean_unique[name]:
            ingredients.loc[i, 'TypeOfIngredient'] = 'заголовок'

# ingredients.to_csv('ingredients_new.csv', index=False)