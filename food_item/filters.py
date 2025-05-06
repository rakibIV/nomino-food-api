from django_filters.rest_framework import FilterSet
from food_item.models import FoodItem

class MenuFilter(FilterSet):
    class Meta:
        model = FoodItem
        fields = {
            'category' : ['exact']
        }