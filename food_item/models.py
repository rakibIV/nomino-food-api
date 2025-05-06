from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=250)
    details = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    

class FoodItem(models.Model):
    name = models.CharField( max_length=250, verbose_name="Food Item Name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = CloudinaryField('image')
    is_special = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    food_item = models.ForeignKey(FoodItem, on_delete= models.CASCADE, related_name='reviews')
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.first_name} on {self.food_item.name} ({self.ratings}/5)"
    



    
