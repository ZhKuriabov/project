# This Python file uses the following encoding: utf-8
import os, sys
import csv
import pandas as pd
import psycopg2
import ast
import json
conn = psycopg2.connect("host=suleiman.db.elephantsql.com dbname=djtnthkl user=djtnthkl password=1CuR4tFpKjezn1d-hHAQAbjhw89ypgdJ port=5432")
cur = conn.cursor()

# cur.execute('SELECT * FROM api_recipes_userprofile')
# one = cur.fetchone()
# all = cur.fetchall()

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

print('Name:', full_recipe['Recipe name'][0], '\n', 'Image link small:', description_recipe['Image small'][0], '\n',
      'Image link big:', full_recipe['Image link'][0], '\n', 'Link:', description_recipe['Recipe Link'][0], '\n',
      'Portions:', full_recipe['Persons'][0], '\n', 'Preparing Time:', full_recipe['Preparing Time'][0], '\n',
      'Cooking Time:', full_recipe['Cooking Time'][0], '\n', 'Difficulty:', full_recipe['Difficulty'][0])
