"""LittleLemon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
menu_item_router = DefaultRouter()
menu_item_router.register('', views.MenuItemsView)

manager_group_router = DefaultRouter()
manager_group_router.register("users", views.ManagerGroupView, basename='managers-details')


crew_group_router = DefaultRouter()
crew_group_router.register("users", views.CrewGroupView, basename = 'delivery-crew-details')

urlpatterns = [
    path('home', views.home, name='home'),
    path('menu-items/', include(menu_item_router.urls)),
    path('groups/managers/', include(manager_group_router.urls)),
    path('groups/delivery-crew/', include(crew_group_router.urls)),
    path('cart/menu-items/', views.CartView.as_view(), name= "cart"),
    path('orders/', views.OrderView.as_view(), name='order'),
    path('orders/<int:pk>/', views.OrderById.as_view(), name='order-id'),
    
    
]
