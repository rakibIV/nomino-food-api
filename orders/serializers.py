from rest_framework import serializers
from orders.models import Cart, CartItem, Order, OrderItem
from food_item.models import FoodItem
from orders.services import OrderServices





class SimpleFoodItem(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['name','price']
        

        
        
class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['food_item','quantity']
        
        


class CartItemSerializer(serializers.ModelSerializer):
    item = SimpleFoodItem(source='food_item',read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = CartItem
        fields = ['id','cart','food_item','item','quantity','total_price']
        read_only_fields = ['cart','item']
        extra_kwargs = {
            'food_item': {'write_only': True}
        }
        
        
    def get_total_price(self, instance):
        return instance.quantity * instance.food_item.price
        
    
    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        cart = Cart.objects.get(id=cart_id)
        food_item = validated_data.get('food_item')
        quantity = validated_data.get('quantity')
        if CartItem.objects.filter(cart=cart, food_item=food_item).exists():
            cart_item = CartItem.objects.filter(cart= cart, food_item=food_item).first()
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
            
        else:
            return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only = True)
    class Meta:
        model = Cart
        fields = ['id','user','items']
        read_only_fields = ['user']
        
        
        
  


        

class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.get(id=cart_id):
            raise serializers.ValidationError("No cart found with this UUID")
        
        cart = Cart.objects.get(id=cart_id)
        if not CartItem.objects.filter(cart=cart).exists():
            raise serializers.ValidationError("Cart is empty!")
        
        if cart.user != self.context.get('user'):
            raise serializers.ValidationError("You can only create an order for your own cart!")
        
        return cart_id
    def create(self, validated_data):
        user = self.context.get('user')
        cart_id = validated_data.get('cart_id')
        
        try:
            order = OrderServices.create_order(user=user, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
    def to_representation(self, instance):
        return OrderSerializer(instance).data
    
    
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        
        
    def update(self, instance, validated_data):
        user = self.context['user']
        new_status = validated_data['status']
        
        if new_status == Order.CANCELED:
            return OrderServices.cancel_order(user=user, order=instance)
        
        if not user.is_staff:
            raise serializers.ValidationError({'detail':"You are not allowed to update the order!"})
        
        return super().update(instance,validated_data)
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    food_item = SimpleFoodItem(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['food_item','price','quantity','total_price']      

    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','address','user','status','total_price','created_at','items']
        
        
class EmptySerializer(serializers.Serializer):
    pass



