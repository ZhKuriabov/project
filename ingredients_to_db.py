# This Python file uses the following encoding: utf-8
import os, sys
import pandas as pd
import psycopg2

ingredients = pd.read_csv('ingredients.csv')
calorizator = pd.read_csv('calorizator.csv')

similar_name = 0
for i in range(len(ingredients['Name'].unique())):
    for product in range(len(calorizator['Продукт'])):
        if ingredients['Name'].unique()[i] == calorizator['Продукт'][product]:
            similar_name += 1
print(similar_name)
# print(len(ingredients['Name'].unique()))
    # if ingredients['TypeOfIngredient'][i] == str('!!!'):
    #     print(ingredients['Name'][i], ingredients['Index'][i])