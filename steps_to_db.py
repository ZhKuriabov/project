import pandas as pd
import psycopg2

# id
# step
# recipe_id

#preparing data for db uploading
full_recipe = pd.read_csv('full_information.csv')

conn = psycopg2.connect("host=suleiman.db.elephantsql.com "
                        "dbname=djtnthkl "
                        "user=djtnthkl "
                        "password=1CuR4tFpKjezn1d-hHAQAbjhw89ypgdJ "
                        "port=5432")
cur = conn.cursor()

for i in range(len(full_recipe)):
    s = full_recipe['Recipe steps'][i]
    s = ''.join(c for c in s if c not in ['n', 'r', '\\'])
    s = s.replace('xa0', '').replace('.', '. ').replace('. )', '.)')
    s = s.split("'")
    s = [s[each] for each in range(len(s)) if len(s[each]) > 2]
    for j in range(len(s)):
        cur.execute("insert into api_recipes_recipestep (step, recipe_id_id) values (%s, %s)",\
                    (s[j], i + 1))

conn.commit()

cur.execute('SELECT * FROM api_recipes_recipestep')
rows = cur.fetchall()

for r in rows:
    print(f'id {r[0]} step {r[1]} recipe_id_id {r[2]}')


cur.close()
conn.close()