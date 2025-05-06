from django.urls import path,include
from rest_framework_nested import routers

from food_item.views import FoodItemViewSet, CategoryViewSet, ReviewViewSet, SpecialFoodItemViewSet
from orders.views import CartViewSet, CartItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register('food_items', FoodItemViewSet, basename='food_item')
router.register('categories', CategoryViewSet, basename='category')
router.register('carts', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='order')
router.register('special_foods', SpecialFoodItemViewSet, basename='special-food')
# router.register('reviews', ReviewViewSet, basename='review')

food_item_router = routers.NestedDefaultRouter(router, 'food_items', lookup='food_item')
food_item_router.register('reviews', ReviewViewSet, basename='food-items-review')
cart_router = routers.NestedDefaultRouter(router,'carts', lookup='cart')
cart_router.register('items',CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('',include(router.urls)),
    path('', include(food_item_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt'))
]
