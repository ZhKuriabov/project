import requests
from bs4 import BeautifulSoup
import csv

CSV = 'general_information.csv'
CSV_INGREDIENTS = 'ingredients.csv'

HOST = 'https://eda.ru/'
URL = 'https://eda.ru/recepty'

HOST1 = 'https://cooklikemary.ru/'
URL1 = 'https://cooklikemary.ru/recipe'

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
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        for td in tr.find_all('td'):
            if td != 2:
                name = tr.find('td').get('title')
                rows.append(
                    {
                        f'{name}': td.find('div', class_='field-items').get_text(strip=True),
                    }
                ) # data row
    return rows

def get_second_table_data_text(table):
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        for td in tr.find_all('td'):
            name = td.find('td').get('title')
            rows.append(
                {
                    f'{name}': td.find('div', class_='field-item').get_text(strip=True),
                }
            ) # data row
    return rows

def get_recipe_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    recipes = []

    main_table = soup.find_all('table')[0] # Grab the first table
    ingredients_table = soup.find_all('table')[1]  # Grab the second table

    recipes.append(
        {
            'recipe_name': soup.find('div', class_='page-title').find('h2').get_text(strip=True),
            'main_information': get_first_table_data_text(main_table),
            'ingredient': get_second_table_data_text(ingredients_table),
            'recipe_img': soup.find('div', class_='slick').find('a').get('href')
        }
    )
    return recipes

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Recipe name', 'Recipe Link', 'Image'])
        for item in items:
            writer.writerow([item['title'], item['link_recipe'], item['recipe_img']])

def save_pecipe_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Recipe name', 'Ingredients', 'Image link', 'Main information'])
        for item in items:
            writer.writerow([item['recipe_name'], item['ingredient'], item['recipe_img'], item['main_information']])

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
        for page in range(0, len(recipe_links)):
            html = get_html(recipe_links[page])
            print(f'Parsing the page:  {page}')
            recipes.extend(get_recipe_content(html.text))
            print(recipes[-1])
            save_pecipe_doc(recipes, CSV_INGREDIENTS)
    else:
        print('Error')

parsing_each_recipe()