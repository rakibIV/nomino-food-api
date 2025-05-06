from orders.models import Order, OrderItem, Cart, CartItem
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

class OrderServices:
    
    
    @staticmethod
    def create_order(user, cart_id):
        
        with transaction.atomic():
            cart = Cart.objects.get(id=cart_id)
            cart_items = CartItem.objects.select_related('food_item').filter(cart=cart)
            total_price = sum([item.food_item.price*item.quantity for item in cart_items])
            address = getattr(user, 'address', "User don't have any address yet!")
            order = Order.objects.create(user=user, total_price=total_price, address=address)
            
            order_items = [
                    OrderItem(
                        order = order,
                        food_item = item.food_item,
                        price = item.food_item.price,
                        quantity = item.quantity,
                        total_price = item.food_item.price*item.quantity
                    )
                    for item in cart_items
                ]
            
            OrderItem.objects.bulk_create(order_items)
            
            cart.delete()
            return order
        
        
    @staticmethod
    def cancel_order(user,order):
        if user.is_staff:
            order.status = Order.CANCELED
            order.save()
            return order
        
        if user != order.user:
            raise PermissionDenied({"detail" : "You can only cancel your own order!"})
        
        if order.status == Order.DELIVERED:
            raise ValidationError({'detail':"Your product is already delivered. You can't cancel the order now!"})
        
        order.status = Order.CANCELED
        order.save()
        return order
        