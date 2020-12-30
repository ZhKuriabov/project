import requests
from bs4 import BeautifulSoup
import csv

CSV = 'general_information.csv'
CSV_INGREDIENTS = 'full_information.csv'
CSV_TEST = 'test.csv'

HOST = 'https://eda.ru/'
URL = 'https://eda.ru/recepty'

HOST1 = 'https://cooklikemary.ru/'
URL1 = 'https://cooklikemary.ru/filter/384+49+639+447+414+50+1+142+25+26+176+625+27+38+131+39+40+51+20+52+54+55+107+78'
#'https://cooklikemary.ru/recipe'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

HEADERS1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS1, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='views-row') #tile-list__horizontal-tile for cooklikemary.ru
    recipes = []

    for item in items:
        recipes.append(
            {
                'title': item.find('div', class_='recipe-description').find('h3').get_text(strip=True),
                'link_recipe': HOST1 + item.find('div', class_='node').find('a').get('href'),
                'recipe_img': item.find('div', class_='node').find('img').get('src')
            }
        )
    return recipes

def get_first_table_data_text(table):
    rows = {}
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.update(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        for td in tr.find_all('td'):
            name = td.get('title')
            # print(name, type(name))
            if name != 'Сложность рецепта':
                try:
                    rows.update(
                        {
                            f'{name}': td.find('div', class_='field-items').get_text(strip=True),
                        }
                    ) # data row
                except:
                    continue
            else:
                count = 0
                divs = td.find_all('div', class_='star')
                for div in divs:
                    if div.find('span', class_='on'):
                        count += 1
                rows.update(
                    {
                        'Сложность рецепта': str(count)
                    }
                )

    return rows

def get_second_table_data_text(table):
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs:# for every table row
        td = tr.find_all('td')
        if len(td) > 1:
            # for td in tr.find_all('td'):
            try:
                rows.append(
                    {
                        f'{td[1].get_text(strip=True)}': td[2].get_text(strip=True)
                    }
                )# data row
            except:
                rows.append(
                    {
                        f'{td[1].get_text(strip=True)}': ''
                    }
                )# data row

        else:
            rows.append(
                {
                    'Title': td[0].get_text(strip=True)
                }
            )

    return rows

def get_recipe_steps(recipe_steps):
    steps = []
    for step in recipe_steps:
        steps.append(step.get_text(strip=True))
    return steps


def get_recipe_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    recipes = []

    main_table = soup.find_all('table')[0] # Grab the first table
    ingredients_table = soup.find_all('table')[1]  # Grab the second table
    recipe_steps = soup.find_all('div', class_='step-text')

    recipes.append(
        {
            'recipe_name': soup.find('div', class_='page-title').find('h2').get_text(strip=True),
            'recipe_steps': get_recipe_steps(recipe_steps),
            'ingredient': get_second_table_data_text(ingredients_table),
            'recipe_img': soup.find('div', class_='slick').find('a').get('href')
        }
    )
    recipes = [dict(item, **get_first_table_data_text(main_table)) for item in recipes]

    return recipes

def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Recipe name', 'Recipe Link', 'Image small'])
        for item in items:
            writer.writerow([item['title'], item['link_recipe'], item['recipe_img']])

def save_pecipe_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Recipe name', 'Ingredients', 'Image link', 'Preparing Time', 'Cooking Time', 'Difficulty', 'Persons', 'Recipe steps'])
        for item in items:
            try:
                writer.writerow([item['recipe_name'], item['ingredient'], item['recipe_img'], item['Время подготовки'],
                                 item['Время готовки'], item['Сложность рецепта'],
                                 item['На какое количество человек расчитан рецепт'], item['recipe_steps']])
            except:
                writer.writerow([item['recipe_name'], item['ingredient'], item['recipe_img'], 0,
                                 item['Время готовки'], item['Сложность рецепта'],
                                 item['На какое количество человек расчитан рецепт'], item['recipe_steps']])

def parser_cooklikemary():
    PAGENATION = input('Number of pages for parsing: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL1)

    if html.status_code == 200:
        recipe = []
        for page in range(0, PAGENATION):
            if page == 0:
                html = get_html(URL1)
            else:
                html = get_html(URL1, params={'page': page})
            print(f'Parsing the page:  {page}')
            recipe.extend(get_content(html.text))
            save_doc(recipe, CSV)
    else:
        print('Error')

def parsing_each_recipe():
    PAGENATION = input('Number of pages for parsing: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL1)
    recipe = []
    for page in range(0, PAGENATION):
        if page == 0:
            html = get_html(URL1)
        else:
            html = get_html(URL1, params={'page': page})
        print(f'Parsing the page:  {page}')
        recipe.extend(get_content(html.text))

    recipe_links = []

    for item in recipe:
        recipe_links.append(item["link_recipe"])

    if html.status_code == 200:
        recipes = []
        for recipe_number in range(0, len(recipe_links)):
            try:
                html = get_html(recipe_links[recipe_number])
                print(f'Parsing the recipe:  {recipe_number}')
                recipes.extend(get_recipe_content(html.text))
                # print(recipes[-1])
                save_pecipe_doc(recipes, CSV_INGREDIENTS)
            except:
                print('Pass the recipe!')
                continue
    else:
        print('Error')

# parser_cooklikemary()
# parsing_each_recipe()