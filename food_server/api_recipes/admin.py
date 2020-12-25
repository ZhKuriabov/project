from django.contrib import admin
from .models import *

Models = (Recipe, UserProfile, Product, Ingredient, userprofile_recipe)
admin.site.register(Models)