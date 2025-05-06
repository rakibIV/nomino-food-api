from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from food_item.models import FoodItem, Category, Reviews
from food_item.serializers import FoodItemSerializer,FoodItemCreateSerializer, CategorySerializer,ReviewSerializer, SpecialFoodItemSerializer, SpecialFoodItemUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from food_item.filters import MenuFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from food_item.pagination import DefaultPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


class FoodItemViewSet(ModelViewSet):
    """
    API endpoint for managing food items.

    """
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.select_related('category').all().order_by('id')
    filterset_class = MenuFilter
    pagination_class = DefaultPagination
    search_fields = ['name']

    @swagger_auto_schema(
        operation_summary="Return all food items, ordered by most recently added.",
        operation_description="Supports filtering by category and searching by name.",
        responses={
            200: openapi.Response(
                description="List of food items",
                schema=FoodItemSerializer(many=True)
            ),
            401: "Authentication credentials were not provided."
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Return a food item instance.",
        responses={
            200: openapi.Response(
                description="Food item details",
                schema=FoodItemSerializer()
            ),
            404: "Food item not found."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new food item.",
        operation_description="Only admin users can create food items.",
        responses={
            201: openapi.Response(
                description="Food item created successfully",
                schema=FoodItemSerializer()
            ),
            400: "Validation error",
            403: "You do not have permission to perform this action."
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a food item.",
        operation_description="Only admin users can update food items.",
        responses={
            200: openapi.Response(
                description="Food item updated successfully",
                schema=FoodItemSerializer()
            ),
            400: "Validation error",
            403: "You do not have permission to perform this action.",
            404: "Food item not found."
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a food item with partial data.",
        operation_description="Only admin users can partially update food items.",
        responses={
            200: openapi.Response(
                description="Food item updated successfully",
                schema=FoodItemSerializer()
            ),
            400: "Validation error",
            403: "You do not have permission to perform this action.",
            404: "Food item not found."
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a food item.",
        operation_description="Only admin users can delete food items.",
        responses={
            204: "Food item deleted successfully.",
            403: "You do not have permission to perform this action.",
            404: "Food item not found."
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return FoodItemCreateSerializer
        return FoodItemSerializer
    
    
class CategoryViewSet(ModelViewSet):
    """
    API endpoint for managing food categories.
    """
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    @swagger_auto_schema(
        operation_summary="Return all categories.",
        responses={
            200: openapi.Response(
                description="List of categories",
                schema=CategorySerializer(many=True)
            ),
            401: "Authentication credentials were not provided."
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Return a category instance.",
        responses={
            200: openapi.Response(
                description="Category details",
                schema=CategorySerializer()
            ),
            404: "Category not found."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new category.",
        operation_description="Only admin users can create categories.",
        responses={
            201: openapi.Response(
                description="Category created successfully",
                schema=CategorySerializer()
            ),
            400: "Validation error",
            403: "You do not have permission to perform this action."
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a category.",
        operation_description="Only admin users can update categories.",
        responses={
            200: openapi.Response(
                description="Category updated successfully",
                schema=CategorySerializer()
            ),
            400: "Validation error",
            403: "You do not have permission to perform this action.",
            404: "Category not found."
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a category with partial data.",
        operation_description="Only admin users can partially update categories.",
        responses={
            200: openapi.Response(
                description="Category updated successfully",
                schema=CategorySerializer()
            ),
            400: "Validation error",
            403: "You do not have permission to perform this action.",
            404: "Category not found."
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a category.",
        operation_description="Only admin users can delete categories.",
        responses={
            204: "Category deleted successfully.",
            403: "You do not have permission to perform this action.",
            404: "Category not found."
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
    
class ReviewViewSet(ModelViewSet):
    """
    API endpoint for managing food item reviews.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Return all reviews for a specific food item.",
        responses={
            200: openapi.Response(
                description="List of reviews",
                schema=ReviewSerializer(many=True)
            ),
            401: "Authentication credentials were not provided."
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Return a review instance for a specific food item.",
        responses={
            200: openapi.Response(
                description="Review details",
                schema=ReviewSerializer()
            ),
            404: "Review not found."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new review for a food item.",
        operation_description="Users can only submit one review per food item.",
        responses={
            201: openapi.Response(
                description="Review created successfully",
                schema=ReviewSerializer()
            ),
            400: "You have already submitted a review for this food item.",
            401: "Authentication credentials were not provided."
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a review.",
        operation_description="Users can only update their own reviews.",
        responses={
            200: openapi.Response(
                description="Review updated successfully",
                schema=ReviewSerializer()
            ),
            400: "Validation error",
            403: "You can update only your reviews!",
            404: "Review not found."
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a review with partial data.",
        operation_description="Users can only update their own reviews.",
        responses={
            200: openapi.Response(
                description="Review updated successfully",
                schema=ReviewSerializer()
            ),
            400: "Validation error",
            403: "You can update only your reviews!",
            404: "Review not found."
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a review.",
        operation_description="Users can only delete their own reviews.",
        responses={
            204: "Review deleted successfully.",
            403: "You can delete only your reviews!",
            404: "Review not found."
        }
    )
    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if request.user.is_staff or review.user == request.user:
            return super().destroy(request, *args, **kwargs)

        raise PermissionDenied("You do not have permission to delete this review.")

    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    def get_queryset(self):
        food_item_id = self.kwargs.get('food_item_pk') 
        
        return Reviews.objects.filter(food_item_id=food_item_id)
    
    def get_serializer_context(self):
        return {'food_item_id':self.kwargs.get('food_item_pk'), 'user':self.request.user}
    
    
    
    
class SpecialFoodItemViewSet(GenericViewSet,ListModelMixin,RetrieveModelMixin,UpdateModelMixin):
    """
    API endpoint for managing special food items.
    """
    permission_classes = [IsAuthenticated]
    queryset = FoodItem.objects.filter(is_special=True)

    @swagger_auto_schema(
        operation_summary="Return all special food items.",
        responses={
            200: openapi.Response(
                description="List of special food items",
                schema=SpecialFoodItemSerializer(many=True)
            ),
            401: "Authentication credentials were not provided."
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Return a special food item instance.",
        responses={
            200: openapi.Response(
                description="Special food item details",
                schema=SpecialFoodItemSerializer()
            ),
            404: "Special food item not found."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a special food item's status.",
        operation_description="Only admin users can update special food items.",
        responses={
            200: openapi.Response(
                description="Special food item updated successfully",
                schema=SpecialFoodItemUpdateSerializer()
            ),
            400: "You do not have permission to update this item.",
            403: "You do not have permission to perform this action.",
            404: "Special food item not found."
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a special food item's status with partial data.",
        operation_description="Only admin users can partially update special food items.",
        responses={
            200: openapi.Response(
                description="Special food item updated successfully",
                schema=SpecialFoodItemUpdateSerializer()
            ),
            400: "You do not have permission to update this item.",
            403: "You do not have permission to perform this action.",
            404: "Special food item not found."
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return SpecialFoodItemUpdateSerializer
        return SpecialFoodItemSerializer
    
    def get_serializer_context(self):
        return {'user':self.request.user}
    
