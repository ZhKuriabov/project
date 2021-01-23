# This Python file uses the following encoding: utf-8
import os, sys
import requests
import re
import pandas as pd
from unicodedata import normalize

description_recipe = pd.read_csv('general_information.csv')
recipe_link = description_recipe['Recipe Link']
df_list = []
index = []
type_of_ingredient = []
for i in range(328):
    URL = recipe_link[i]
    r = requests.get(URL)
    # print(i)
    recipe_ingredients = pd.read_html(r.text)[1]
    # print(recipe_ingredients)
    for j in range(len(recipe_ingredients[2])):
        try:
            new_value = recipe_ingredients[2][j].split()[-2:].copy()
            full = recipe_ingredients[2][j]
        except:
            new_value = ''
            full = ''

        if len(new_value) > 1 and "гр." in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            new_value[0] = normalize('NFKC', new_value[0]).replace("⁄", "/")
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value = ''
            new_value += all_integers_in_str[0]
            # new_value += ' гр.'
            type_of_ingredient.append('гр.')
            # new_value = new_value.split(' ')
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "кг." in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            new_value[0] = normalize('NFKC', new_value[0]).replace("⁄", "/")
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value = ''
            new_value += all_integers_in_str[0]
            # new_value += ' кг.'
            type_of_ingredient.append('кг.')
            # new_value = new_value.split(' ')
        elif len(new_value) > 1 and "шт." in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            new_value[0] = normalize('NFKC', new_value[0]).replace("⁄", "/")
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
            try:
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
                new_value = ''
                new_value += all_integers_in_str[0]
                # new_value += ' шт.'
                type_of_ingredient.append('шт.')
                # new_value = new_value.split(' ')
            except:
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value = ''
                new_value += all_integers_in_str[-1]
                # new_value += ' шт.'
                type_of_ingredient.append('шт.')
                # new_value = new_value.split(' ')
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "мл." in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            new_value[0] = normalize('NFKC', new_value[0]).replace("⁄", "/")
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value = ''
            new_value += all_integers_in_str[0]
            # new_value += ' мл.'
            type_of_ingredient.append('мл.')
            # new_value = new_value.split(' ')
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "ст.л" in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            new_value[0] = normalize('NFKC', new_value[0]).replace("⁄", "/")
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1/numbers[k]}')
            try:
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
                new_value = ''
                # print('i: ', i, 'j: ', j, all_integers_in_str)
                new_value += all_integers_in_str[0]
                # new_value += ' ст.л.'
                type_of_ingredient.append('ст.л.')
                # new_value = new_value.split(' ')
            except:
                try:
                    all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                    new_value = ''
                    new_value += all_integers_in_str[-1]
                    # new_value += ' ст.л.'
                    type_of_ingredient.append('ст.л.')
                    # new_value = new_value.split(' ')
                except:
                    if 'пол' in new_value:
                        all_integers_in_str = '0.5'
                        new_value = ''
                        new_value += all_integers_in_str[-1]
                        # new_value += ' ст.л.'
                        type_of_ingredient.append('ст.л.')
                        # new_value = new_value.split(' ')
        elif len(new_value) > 1 and "ч.л" in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            new_value[0] = normalize('NFKC', new_value[0]).replace("⁄", "/")
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1/numbers[k]}')
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value = ''
            try:
                new_value += all_integers_in_str[0]
                # new_value += ' ч.л.'
                type_of_ingredient.append('ч.л.')
                # new_value = new_value.split(' ')
            except:
                new_value = 0
                # new_value += ' ч.л.'
                # new_value = new_value.split(' ')
                type_of_ingredient.append('мало')
        else:
            # new_value = full
            if full.count('гр.') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                full = normalize('NFKC', full).replace("⁄", "/")
                for k in range(len(numbers)):
                    full = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                # print('i: ', i, 'j: ', j, all_integers_in_str)
                try:
                    all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                    new_value = ''
                    new_value += all_integers_in_str[0]
                    # new_value += ' гр.'
                    type_of_ingredient.append('гр.')
                    # new_value = new_value.split(' ')
                except:
                    all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                    new_value = ''
                    new_value += all_integers_in_str[-1]
                    # new_value += ' гр.'
                    type_of_ingredient.append('гр.')
                    # new_value = new_value.split(' ')
                # print('Warning гр!', new_value)
            elif full.count('кг.') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                full = normalize('NFKC', full).replace("⁄", "/")
                for k in range(len(numbers)):
                    full = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                # print('i: ', i, 'j: ', j, all_integers_in_str)
                try:
                    all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                    new_value = ''
                    new_value += all_integers_in_str[0]
                    # new_value += ' кг.'
                    type_of_ingredient.append('кг.')
                    # new_value = new_value.split(' ')
                except:
                    all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                    new_value = ''
                    new_value += all_integers_in_str[-1]
                    # new_value += ' кг.'
                    type_of_ingredient.append('кг.')
                    # new_value = new_value.split(' ')
            elif full.count('шт.') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                full = normalize('NFKC', full).replace("⁄", "/")
                for k in range(len(numbers)):
                    full = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value = ''
                new_value += all_integers_in_str[0]
                # new_value += ' шт.'
                type_of_ingredient.append('шт.')
                # new_value = new_value.split(' ')
                # print('Warning шт!', new_value)
            elif full.count('мл') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                full = normalize('NFKC', full).replace("⁄", "/")
                for k in range(len(numbers)):
                    full = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value = ''
                new_value += all_integers_in_str[0]
                # new_value += ' мл.'
                type_of_ingredient.append('мл.')
                # new_value = new_value.split(' ')
                # print('Warning мл!', new_value)

            elif full.count('ч.л') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                full = normalize('NFKC', full).replace("⁄", "/")
                for k in range(len(numbers)):
                    full = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value = ''
                # print('i: ', i, 'j: ', j, all_integers_in_str)
                try:
                    new_value += all_integers_in_str[0]
                    # new_value += ' ч.л.'
                    type_of_ingredient.append('ч.л.')
                    # new_value = new_value.split(' ')
                except:
                    new_value = 0
                    # new_value += ' ч.л.'
                    # new_value = new_value.split(' ')
                    type_of_ingredient.append('мало')
                # print('Warning ч.л.!', new_value)
            elif full.count('ст.л.') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                full = normalize('NFKC', full).replace("⁄", "/")
                # print('full', full)
                for k in range(len(numbers)):
                    full = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value = ''
                # print('i: ', i, 'j: ', j, all_integers_in_str)
                new_value += all_integers_in_str[0]
                # new_value += ' ст.л.'
                type_of_ingredient.append('ст.л.')
                # new_value = new_value.split(' ')
                # print('Warning ст.л.!', new_value)

            elif ('1' or '2' or '3' or '4' or '5' or '6' or '7') in full:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                full = normalize('NFKC', full).replace("⁄", "/")
                for k in range(len(numbers)):
                    full = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value = ''
                new_value += all_integers_in_str[0]
                # new_value += ' шт.'
                type_of_ingredient.append('шт.')
                # new_value = new_value.split(' ')
                # print('Dangerous!', new_value)
            else:
                new_value = 0
                # new_value += full
                type_of_ingredient.append('по вкусу')
                # print('???', full)

        index.append(i)

        if len(type_of_ingredient) < len(index):
            type_of_ingredient.append('!!!')
            print('!!!', i, j)

        recipe_ingredients[2][j] = new_value

        # recipe_ingredients[2][j] = re.findall(r'\d*\.\d+|\d+', str(recipe_ingredients[2][j]))
        # recipe_ingredients[2][j] = ' '.join([str(elem) for elem in recipe_ingredients[2][j]])
    print(i)
    df_list.append(recipe_ingredients)

print('Len of type_of_ingredient : ', len(type_of_ingredient))
print('Len of index : ', len(index))

df = pd.concat(df_list)
print('Len of db : ', len(df))
df['type_of_ingredient'] = type_of_ingredient
df['index'] = index

del df[0]
df.columns = ['Name', 'Weight', 'TypeOfIngredient', 'Index']
print(df)
df.to_csv('ingredients.csv', index=False)