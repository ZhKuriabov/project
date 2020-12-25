import requests
from bs4 import BeautifulSoup
import csv

CSV = 'recipes.csv'

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
    items = soup.find_all('div', class_='views-row') #tile-list__horizontal-tile for eda.ru
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

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Recipe name', 'Recipe Link', 'Image'])
        for item in items:
            writer.writerow([item['title'], item['link_recipe'], item['recipe_img']])


def parser_cooklikemary():
    PAGENATION = input('Number of pages for parsing: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL1)
    if html.status_code == 200:
        recipes = []
        for page in range(0, PAGENATION):
            if page == 0:
                html = get_html(URL1)
            else:
                html = get_html(URL1, params={'page': page})
            print(f'Parsing the page:  {page}')
            recipes.extend(get_content(html.text))
            save_doc(recipes, CSV)
    else:
        print('Error')

parser_cooklikemary()