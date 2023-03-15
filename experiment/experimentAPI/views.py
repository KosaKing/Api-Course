from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
# Create your views here.

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SpecyficMenuItemView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# Deserialization and validation - this is where i stopped 