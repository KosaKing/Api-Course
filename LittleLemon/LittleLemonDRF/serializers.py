from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = MenuItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    menuitem = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


# Cos jest nie tak 

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    delivery_crew = UserSerializer()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'




