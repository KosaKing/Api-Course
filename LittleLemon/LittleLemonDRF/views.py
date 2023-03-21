from rest_framework import generics, permissions, authentication
from .models import Category, MenuItem, Cart, Order, OrderItem, User
from .serializers import UserSerializer, CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.views import APIView

# Create your views here.

# User registration and token generation endpoints 
# XXX
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ListMenu(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ListMenuItem(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

