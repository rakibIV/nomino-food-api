from rest_framework import serializers
from food_item.models import FoodItem, Category, Reviews



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','details','created_at']
        
class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
        
        
class FoodItemCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = FoodItem
        fields = ['id','name','category','description','price','image','is_special']

class FoodItemSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()
    class Meta:
        model = FoodItem
        fields = ['id','name','category','description','price','image','is_special']
        
        
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id','user','food_item','ratings','comment']
        read_only_fields = ['user','food_item']
        
    def create(self, validated_data):
        user = self.context.get('user')
        food_item_id = self.context.get('food_item_id')
        
        print(user, food_item_id)
        
        if Reviews.objects.filter(user=user, food_item_id=food_item_id).exists():
            raise serializers.ValidationError("You have already submitted a review for this food item.")
        review = Reviews.objects.create(food_item_id=food_item_id, **validated_data)
        return review
    
    def update(self, instance, validated_data):
        user = self.context.get('user')
        
        if instance.user != user:
            raise serializers.ValidationError("You can update only your reviews!")
        
        return super().update(instance, validated_data)
    



    
class SpecialFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id','name', 'price', 'is_special']
        
        
class SpecialFoodItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['is_special']
        
    def update(self, instance, validated_data):
        user = self.context.get('user')
        if not user.is_staff:
            raise serializers.ValidationError("You do not have permission to update this item.")
        
        return super().update(instance,validated_data)
