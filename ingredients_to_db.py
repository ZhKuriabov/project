import requests
import re
import pandas as pd

description_recipe = pd.read_csv('general_information.csv')
recipe_link = description_recipe['Recipe Link']
df_list = []
for i in range(200):
    URL = recipe_link[i]
    r = requests.get(URL)
    # print(i)
    recipe_ingredients = pd.read_html(r.text)[1]
    # print(recipe_ingredients)
    for j in range(len(recipe_ingredients[2])):

        new_value = recipe_ingredients[2][j].split()[-2:].copy()
        full = recipe_ingredients[2][j]

        if len(new_value) > 1 and "гр." in new_value[1]:
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value[0] = all_integers_in_str[0]
            new_value[1] = "гр."
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "шт." in new_value[1]:
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            print('Recipe #', i, 'lll', j, all_integers_in_str)
            new_value = ''
            new_value += all_integers_in_str[0]
            new_value += ' шт.'
            new_value = new_value.split(' ')
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "мл." in new_value[1]:
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value[0] = all_integers_in_str[0]
            new_value[1] = "мл."
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "долька" in new_value[1]:
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value[0] = all_integers_in_str[0]
            new_value[1] = "долька"
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "ст.л" in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1/numbers[k]}')

            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value[0] = all_integers_in_str[0]
            new_value[1] = "ст.л."
            # print(f'{i}: ', new_value)
        elif len(new_value) > 1 and "ч.л" in new_value[1]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for k in range(len(numbers)):
                new_value[0] = new_value[0].replace(f'1/{numbers[k]}', f'{1/numbers[k]}')
            all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(new_value))
            new_value[0] = all_integers_in_str[0]
            new_value[1] = "ч.л."
        else:
            # new_value = full
            if full.count('гр') != 0:
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value[0] = all_integers_in_str[0]
                new_value[1] = 'гр'
                print('Warning гр!', new_value)
            elif full.count('шт') != 0:
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value[0] = all_integers_in_str[0]
                new_value[1] = 'шт'
                print('Warning шт!', new_value)
            elif full.count('мл') != 0:
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value[0] = all_integers_in_str[0]
                new_value[1] = 'мл'
                print('Warning мл!', new_value)

            elif full.count('ч.л') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for k in range(len(numbers)):
                    new_value = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value = ''
                new_value += all_integers_in_str[0]
                new_value += ' ч.л.'
                new_value = new_value.split(' ')
                print('Warning ч.л.!', new_value)

            elif full.count('ст.л') != 0:
                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for k in range(len(numbers)):
                    new_value = full.replace(f'1/{numbers[k]}', f'{1 / numbers[k]}')
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                del new_value
                new_value = ''
                new_value += all_integers_in_str[0]
                new_value += ' ст.л.'
                new_value = new_value.split(' ')
                print('Warning ст.л.!', new_value)

            elif ('1' or '2' or '3' or '4' or '5' or '6' or '7') in full:
                all_integers_in_str = re.findall(r'\d*\.\d+|\d+', str(full))
                new_value[0] = all_integers_in_str[0]
                new_value[1] = 'шт.'
                print('Dangerous!', new_value)
            else:
                new_value[0] = full
                # print('???', full)

        # recipe_ingredients[2][j] = new_value

        # recipe_ingredients[2][j] = re.findall(r'\d*\.\d+|\d+', str(recipe_ingredients[2][j]))
        # recipe_ingredients[2][j] = ' '.join([str(elem) for elem in recipe_ingredients[2][j]])

    df_list.append(recipe_ingredients)

df = pd.concat(df_list)

del df[0]

# print(df)
df.to_csv('test.csv', index=False)