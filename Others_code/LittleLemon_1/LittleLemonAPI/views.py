from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .permission import *
from .models import *

from .serializers import *

# Create your views here.
def home(request):
    return HttpResponse('This is the home page')

class MenuItemsView(ModelViewSet):
    # allowed_methods = ['GET', 'POST','PATCH', 'PUT', 'DELETE']
    user = User.objects.get(username = 'shayan')
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_field = "slug"
    filterset_fields = ['category']
    search_fields = ['title', 'category__title']
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsManager()]
        else:
            return []
    
class ManagerGroupView(ModelViewSet):
    permission_classes = [IsManager]
    serializer_class = GroupManagerSerializer
    lookup_field = "username"
    allowed_methods = ['GET', 'POST', 'DELETE']
    def get_queryset(self):
        group = Group.objects.get(name__iexact = 'manager')
        queryset = group.user_set.all()
        return queryset
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            username = serializer.validated_data.get('username')
            user = User.objects.get(username = username)
            group = Group.objects.get(name__iexact = 'manager')
            group.user_set.add(user)
            return Response('user added to the manager group Successfully.', status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        group = Group.objects.get(name__iexact = 'manager')
        group.user_set.remove(instance)
        return Response({"success": "User is removed from the manager role."}, status=status.HTTP_202_ACCEPTED)
    
class CrewGroupView(ModelViewSet):
    permission_classes = [IsManager]
    serializer_class = GroupManagerSerializer
    lookup_field = "username"
    allowed_methods = ['GET', 'POST', 'DELETE']
    def get_queryset(self):
        group = Group.objects.get(name__iexact = 'delivery crew')
        queryset = group.user_set.all()
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            username = serializer.validated_data.get('username')
            user = User.objects.get(username = username)
            group = Group.objects.get(name__iexact = 'delivery crew')
            group.user_set.add(user)
            return Response('user added to the delivery crew Successfully.', status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        group = Group.objects.get(name__iexact = 'delivery crew')
        group.user_set.remove(instance)
        return Response({"success": "User is removed from the manager role."}, status=status.HTTP_202_ACCEPTED)
    
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user = request.user)
        try:
            serializer = CartSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Bad request', status= status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        context = {'user': request.user}
        try:
            
            serializer = CartSerializer(data= request.data, context = context)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = str(e)
            raise serializers.ValidationError(error)
    def delete(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user = user)
        if cart_items:
            cart_items.delete()
            return Response('Cart cleard successfully.', status=status.HTTP_204_NO_CONTENT)
        return Response('Cart is alrady empty.', status=status.HTTP_204_NO_CONTENT)
        
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        is_manager = user.groups.filter(name__iexact = 'manager').exists()
        is_crew = user.groups.filter(name__iexact = 'delivery crew').exists()
        if is_manager:
            orders= OrderItem.objects.all()
        elif is_crew:
            user_assigned = Order.objects.filter(delivery_crew = user).values_list('user')
            orders = []
            orders = [orders.extend(OrderItem.objects.filter(order = usr)) for usr in user_assigned]
        else:
            
            orders = OrderItem.objects.filter(order = user)
        try:
            serializer = OrderItemSerializer(orders, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user = user)
        cart_list = list(cart)
        if not cart_list:
            return Response("Cart is empty", status=status.HTTP_204_NO_CONTENT)
        cart_items = []
        order = {}
        for item in cart_list:
            order['quantity']= item.quantity
            order['price']= item.price
            order['unit_price']= item.unit_price
            order['menuitem']= item.menuitem.id
            cart_items.append(order)
            
            # print(data)
        try:
            serializer = OrderItemSerializer(data = cart_items, many = True)
            if serializer.is_valid():
                serializer.save(order= user.id)
                cart.delete()
                return Response('Added to order item succefully', status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = str(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
class OrderById(APIView):
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsManager()]
        if self.request.method == 'PATCH':
            return [IsDeliveryCrew()]
        else:
            return[IsAuthenticated()]
    def get(self, request, pk):
        
        oder_item = get_object_or_404(OrderItem, id = pk)
        if request.user != oder_item.order:
            raise serializers.ValidationError("Wrong order id, You have no order with this id.")
        print(oder_item)
        serializer = OrderItemSerializer(oder_item)
        return Response(serializer.data, status= status.HTTP_200_OK)
    def delete(self, request, pk):
        order_item = get_object_or_404(OrderItem, id = pk)
        order_item.delete()
        return Response('item removed from the order Item', status=status.HTTP_200_OK)
    def patch(self, request, pk):
        return Response('The order staus is updated sucesssfully.', status=status.HTTP_200_OK)