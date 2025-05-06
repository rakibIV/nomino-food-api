from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from orders.serializers import CartSerializer, CartItemSerializer,EmptySerializer, CartItemUpdateSerializer, OrderSerializer, OrderCreateSerializer, UpdateOrderSerializer
from rest_framework.permissions import IsAuthenticated
from orders.models import Cart, CartItem, Order, OrderItem
from rest_framework.decorators import action
from orders.services import OrderServices
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.


class CartViewSet(ModelViewSet):
    """
    API endpoint for managing user shopping carts.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Return cart for the authenticated user.",
        operation_description="Staff users can view all carts.",
        responses={
            200: openapi.Response(
                description="List of carts",
                schema=CartSerializer(many=True)
            ),
            401: "Authentication credentials were not provided."
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Return a cart instance.",
        operation_description="Users can only retrieve their own cart, while staff can retrieve any cart.",
        responses={
            200: openapi.Response(
                description="Cart details",
                schema=CartSerializer()
            ),
            403: "You do not have permission to view this cart.",
            404: "Cart not found."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new cart for the authenticated user.",
        operation_description="A user can have only one cart.",
        responses={
            201: openapi.Response(
                description="Cart created successfully",
                schema=CartSerializer()
            ),
            400: "Validation error",
            401: "Authentication credentials were not provided."
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_summary="Delete a cart.",
        operation_description="Users can only delete their own cart.",
        responses={
            204: "Cart deleted successfully.",
            403: "You do not have permission to delete this cart.",
            404: "Cart not found."
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class CartItemViewSet(ModelViewSet):
    """
    API endpoint for managing cart items within a specific cart.
    """   
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Return all items in the specified cart.",
        responses={
            200: openapi.Response(
                description="List of cart items",
                schema=CartItemSerializer(many=True)
            ),
            401: "Authentication credentials were not provided.",
            404: "Cart not found."
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Return a cart item instance.",
        responses={
            200: openapi.Response(
                description="Cart item details",
                schema=CartItemSerializer()
            ),
            404: "Cart item not found."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Add a new item to the cart.",
        operation_description="If the item already exists in the cart, the quantity will be incremented.",
        request_body=CartItemSerializer,
        responses={
            201: openapi.Response(
                description="Item added to cart successfully",
                schema=CartItemSerializer()
            ),
            400: "Validation error",
            401: "Authentication credentials were not provided.",
            404: "Cart not found."
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a cart item, typically the quantity.",
        request_body=CartItemUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Cart item updated successfully",
                schema=CartItemSerializer()
            ),
            400: "Validation error",
            404: "Cart item not found."
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a cart item with partial data.",
        request_body=CartItemUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Cart item updated successfully",
                schema=CartItemSerializer()
            ),
            400: "Validation error",
            404: "Cart item not found."
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Remove an item from the cart.",
        responses={
            204: "Cart item removed successfully.",
            404: "Cart item not found."
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
    
    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return CartItemUpdateSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs.get('cart_pk'))
    
    def perform_create(self, serializer):
        cart = Cart.objects.get(id = self.kwargs.get('cart_pk'))
        serializer.save(cart = cart)
        
    def get_serializer_context(self):
        return {'cart_pk':self.kwargs.get('cart_pk')}
    
    
    
class OrderViewSet(ModelViewSet):
    """
    API endpoint for managing orders.
    """
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'option']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Return all orders for the authenticated user.",
        operation_description="Staff users can view all orders.",
        responses={
            200: openapi.Response(
                description="List of orders",
                schema=OrderSerializer(many=True)
            ),
            401: "Authentication credentials were not provided."
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Return an order instance.",
        operation_description="Users can only retrieve their own orders, while staff can retrieve any order.",
        responses={
            200: openapi.Response(
                description="Order details",
                schema=OrderSerializer()
            ),
            403: "You do not have permission to view this order.",
            404: "Order not found."
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new order from a cart.",
        request_body=OrderCreateSerializer,
        responses={
            201: openapi.Response(
                description="Order created successfully",
                schema=OrderSerializer()
            ),
            400: "Validation error - Cart is empty or doesn't exist",
            401: "Authentication credentials were not provided."
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update an order's status.",
        operation_description="Only staff can update order status, except for cancellation.",
        request_body=UpdateOrderSerializer,
        responses={
            200: openapi.Response(
                description="Order updated successfully",
                schema=OrderSerializer()
            ),
            400: "Validation error",
            403: "You are not allowed to update the order!",
            404: "Order not found."
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete an order.",
        responses={
            204: "Order deleted successfully.",
            403: "You do not have permission to delete this order.",
            404: "Order not found."
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Cancel an order.",
        operation_description="Users can cancel their own orders that haven't been delivered. Staff can cancel any order.",
        responses={
            200: openapi.Response(
                description="Order successfully canceled",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Order Canceled"
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Order cannot be canceled",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Your product is already delivered. You can't cancel the order now!"
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Permission denied",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="You can only cancel your own order!"
                        )
                    }
                )
            ),
            404: "Order not found."
        }
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an existing order.
        Users can only cancel their own orders that haven't been delivered yet.
        Staff users can cancel any order.
        """
        order = self.get_object()
        try:
            OrderServices.cancel_order(order=order, user=self.request.user)
        except ValueError as e:
            return ValidationError(str(e))
        return Response({'status': 'Order Canceled'})
    
    def get_serializer_class(self):
        if self.action == "cancel":
            return EmptySerializer
        if self.request.method == "POST":
            return OrderCreateSerializer
        if self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items__food_item").all()
        return Order.objects.prefetch_related("items__food_item").filter(user = self.request.user)
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user':self.request.user}
    
    

    
    



    
    