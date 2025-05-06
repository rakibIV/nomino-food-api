from django.contrib import admin
from food_item.models import FoodItem, Category, Reviews

# Register your models here.

admin.site.register(FoodItem)
admin.site.register(Category)
admin.site.register(Reviews)
