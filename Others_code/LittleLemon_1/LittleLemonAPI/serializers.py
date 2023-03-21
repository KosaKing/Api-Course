from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User, Group
from .models import *

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'category', 'slug']
        # extra_kwargs = {'price': {'max_digits': 6, 'decimal_places': 2}}
        extra_kwargs = {'slug':{"write_only":True}}
        validators = [UniqueTogetherValidator(queryset = MenuItem.objects.all(), fields=['title', 'price', 'category'])]
    def create(self, validated_data):
        return MenuItem.objects.create(**validated_data)
class GroupManagerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 30)
    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {'email': {'read_only':True}}
    def validate_username(self, value):
        user = User.objects.filter(username = value).exists()
        if not user:
            raise serializers.ValidationError("The user doest not exists. Enter a valid user.")
        return value

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    item_slug = serializers.CharField(max_length = 255, write_only = True)
    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity', 'price', 'item_slug','user']
        extra_kwargs = {
            "price": {"read_only":True},
            "quantity": {"max_value":10, "min_value": 1}
        }
    def validate_item_slug(self, value):
        menuitem = MenuItem.objects.filter(slug = value).first()
        if(menuitem is None):
            raise serializers.ValidationError("Menu Item does not exist.")
        return menuitem
    def validate(self, attrs):
        menuitem = attrs['item_slug']
        attrs['menuitem'] = menuitem
        attrs['user']=self.context.get('user')
        attrs['unit_price'] = menuitem.price
        del attrs['item_slug']
        return attrs
        
        
    def create(self, validated_data):
        price = validated_data.get('quantity') * validated_data['unit_price']
        validated_data['price']= price
        return Cart.objects.create(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['__all__']
    
    

class OrderItemSerializer(serializers.ModelSerializer):
    customer_name = serializers.StringRelatedField(source = 'order')
    menu_item = serializers.StringRelatedField(source = 'menuitem')
    # item_slug = serializers.CharField(max_length = 255, write_only = True)
    # menuitem = serializers.SlugRelatedField(slug_field='slug', queryset = MenuItem.objects.all(), write_only =True)
    
    class Meta:
        model = OrderItem
        fields = ['customer_name','menu_item', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            "menuitem": {"write_only": True}
        }
    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)

        
        
class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many= True, read_only = True)
    class Meta:
        model = Order
        fields = ['user', 'delivery_crew', 'status', 'total', 'date', 'orderitem']    