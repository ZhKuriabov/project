# This Python file uses the following encoding: utf-8
import os, sys
import pandas as pd
import psycopg2

ingredients = pd.read_csv('ingredients_new.csv')

# id
# name
# weight
# recipe_id_id
# type_of_ingredient

conn = psycopg2.connect("host=suleiman.db.elephantsql.com "
                        "dbname=djtnthkl "
                        "user=djtnthkl "
                        "password=1CuR4tFpKjezn1d-hHAQAbjhw89ypgdJ "
                        "port=5432")
cur = conn.cursor()

# for i in range(1):
#     cur.execute("insert into api_recipes_ingredient (id, name, weight, recipe_id_id, type_of_ingredient) values (%s, %s, %s, %s, %s)",\
#                 (i + 1, ingredients['Name'][i], int(ingredients['Weight'][i]), int(ingredients['Index'][i]) + 1, ingredients['TypeOfIngredient'][i]))
# for i in range(1, len(ingredients)):
#     cur.execute('update api_recipes_ingredient set id = %s where id = %s', (i + 1, i + 4000))
# conn.commit()

cur.execute('SELECT * FROM api_recipes_ingredient WHERE recipe_id_id = %s', (2,))
rows = cur.fetchall()

for r in rows:
    print(f'id {r[0]} name {r[1]} weight {r[2]} recipe_id_id {r[3]} type_of_ingredient {r[4]}')

cur.close()
conn.close()
