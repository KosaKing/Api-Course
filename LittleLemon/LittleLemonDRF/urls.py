from django.urls import path 
from . import views 

urlpatterns = [ 
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('menu-items/', views.ListMenu.as_view()), 
    path('menu-items/<int:pk>', views.ListMenuItem.as_view()),
] 


# Useful shit 
# week2 - Generic views and ViewSets in DRF