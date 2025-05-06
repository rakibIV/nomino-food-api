from django.db import models
from users.models import User
from food_item.models import FoodItem
from uuid import uuid4
from django.core.validators import MinValueValidator

# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user.first_name} {self.user.last_name}"
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        unique_together = [['cart', 'food_item']]
    
    def __str__(self):
        return f"{self.quantity} X {self.food_item.name}"
    
    
class Order(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled')
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField()
    
    def __str__(self):
        return f"Order {self.id} by {self.user.email} - {self.status}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
    
    

