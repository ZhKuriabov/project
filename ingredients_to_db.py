# This Python file uses the following encoding: utf-8
import os, sys
import pandas as pd
import psycopg2

# Name
# Image link small
# Image link big
# Link
# Portions
# Preparing time
# Cooking time
# Difficulty

description_recipe = pd.read_csv('general_information.csv')
full_recipe = pd.read_csv('full_information.csv')

conn = psycopg2.connect("host=suleiman.db.elephantsql.com "
                        "dbname=djtnthkl "
                        "user=djtnthkl "
                        "password=1CuR4tFpKjezn1d-hHAQAbjhw89ypgdJ "
                        "port=5432")
cur = conn.cursor()

# for i in range(1, len(description_recipe)):
#     cur.execute("insert into api_recipes_recipe (id, name, link, portions, cooking_time, \
#         difficulty, image_link_big, image_link_small, preparing_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",\
#                 (i + 1, full_recipe['Recipe name'][i], description_recipe['Recipe Link'][i], int(full_recipe['Persons'][i]),\
#                  full_recipe['Cooking Time'][i], int(full_recipe['Difficulty'][i]), full_recipe['Image link'][i],\
#                  description_recipe['Image small'][i], full_recipe['Preparing Time'][i]))

# conn.commit()

cur.execute('SELECT * FROM api_recipes_recipe')
rows = cur.fetchall()

for r in rows:
    print(f'id {r[0]} name {r[1]} link {r[2]} portions {r[3]} cooking_time {r[4]} \
    difficulty {r[5]} img_link_big {r[6]} img_link_small {r[7]} preparing_time {r[8]}')

# print('Name:', type(full_recipe['Recipe name'][0]), '\n', 'Image link small:', type(description_recipe['Image small'][0]), '\n',
#       'Image link big:', type(full_recipe['Image link'][0]), '\n', 'Link:', type(description_recipe['Recipe Link'][0]), '\n',
#       'Portions:', type(int(full_recipe['Persons'][0])), '\n', 'Preparing Time:', type(full_recipe['Preparing Time'][0]), '\n',
#       'Cooking Time:', type(full_recipe['Cooking Time'][0]), '\n', 'Difficulty:', type(full_recipe['Difficulty'][0]))

cur.close()
conn.close()

# result=list(set(description_recipe['Recipe name']) ^ set(full_recipe['Recipe name']))
# print(result)
