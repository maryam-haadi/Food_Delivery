from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .permissions import IsOwnerRestuarant,IsOwnerRestuarantCreate,IsRestuarantExist
# Create your views here.
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serializers import *
from .models import *
from rest_framework.response import Response
from  customer.permissions import IsCustomer
from rating.serializers import RatingPostSerializer
from rating.models import Rating
from cart.models import *
from cart.serializers import *
import requests

class RestaurantView(ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.all().filter(owner=user.owner)


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwnerRestuarantCreate()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        elif self.request.method == 'GET':
            return [IsOwnerRestuarant()]
        else:
            return [IsOwnerRestuarant()]


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantShowSerializer
        else:
            return RestaurantPostSerializer


    def create(self, request, *args, **kwargs):
        serializer = RestaurantPostSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            owner = user.owner
            image = serializer.validated_data['image']
            print("image ------",image)
            category = serializer.validated_data['category']
            delivery_time = serializer.validated_data['delivery_time']
            min_cart_price = serializer.validated_data['min_cart_price']
            delivery_price = serializer.validated_data['delivery_price']
            name = serializer.validated_data['name']
            phone_number = serializer.validated_data['phone_number']
            open_time = serializer.validated_data['open_time']
            close_time = serializer.validated_data['close_time']
            address_name = serializer.validated_data['address_name']
            latitude = serializer.validated_data['latitude']
            longitude = serializer.validated_data['longitude']

            restaurant = Restaurant.objects.create(owner=owner,category=category,delivery_time=delivery_time,
                                                   delivery_price=delivery_price,name=name,phone_number=phone_number,
                                                   open_time=open_time,close_time=close_time,address_name=address_name,latitude=latitude,
                                                   longitude=longitude,min_cart_price=min_cart_price)
            restaurant.image = image
            restaurant.save()
            menu = Menu.objects.create(restaurant=restaurant)
            return Response({"message":"create restaurant seccessfully ","data":serializer.data}
                            ,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class FoodViewset(ModelViewSet):
    permission_classes = [IsRestuarantExist]

    def get_queryset(self):
        user = self.request.user
        restaurant = get_object_or_404(Restaurant,owner__user=user)
        menu = get_object_or_404(Menu,restaurant=restaurant)
        return Food.objects.all().filter(menu=menu)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FoodShowSerializer
        else:
            return FoodSerializer



    def create(self, request, *args, **kwargs):
        user = request.user
        restaurant = get_object_or_404(Restaurant,owner__user=user)
        menu = get_object_or_404(Menu,restaurant=restaurant)

        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            food = Food.objects.create(menu=menu,
                                       food_category=serializer.validated_data['food_category'],
                                       image=serializer.validated_data['image'],
                                       name=serializer.validated_data['name'],desc=serializer.validated_data['desc'],
                                       price=serializer.validated_data['price'])
            image = serializer.validated_data['image']
            print(image)
            return Response({"message":"add food seccessfully","data":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request,pk, *args, **kwargs):
        food = get_object_or_404(Food,pk=pk)
        if Order.objects.all().filter(paid=False).filter(restaurant_cart__cart_items__food=food).exists():
            return Response({"message":"yo cant delete this food."},status=status.HTTP_400_BAD_REQUEST)
        else:
            food.delete()
            return Response({"message":"food deleted successfully. "},status=status.HTTP_204_NO_CONTENT)








class FoodCategoryRequestViewset(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):

    permission_classes = [IsRestuarantExist]

    def get_queryset(self):
        return FoodCategoryRequest.objects.all().filter(restaurant__owner__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method =='GET':
            return FoodCategoryRequestShowSerializer
        else:
            return FoodCategoryRequestPostSerializer

    def create(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant,owner__user=request.user)
        serializer = FoodCategoryRequestPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category_request = FoodCategoryRequest.objects.create(restaurant=restaurant,
                                                                  admin_approval=False,
                                                                  **serializer.validated_data)
            return Response({"message":"request post seccessfully","data":serializer.data},status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)







class DeleteRestaurantRequestViewset(GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin):

    permission_classes = [IsRestuarantExist]

    def get_queryset(self):
        return DeleteRestaurantRequest.objects.all().filter(restaurant__owner__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method =='GET':
            return DeleteRestaurantRequestShowSerializer
        else:
            return DeleteRestaurantRequestPostSerializer

    def create(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant,owner__user=request.user)
        serializer = DeleteRestaurantRequestPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            delete_request = DeleteRestaurantRequest.objects.create(restaurant=restaurant,admin_approval=False,
                                                                    desc=serializer.validated_data['desc'])
            return Response({"message":"request post seccessfully","data":serializer.data},status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class FoodCategoryViewset(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [AllowAny]

    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer



url = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
class RestaurantsOrderViewset(ModelViewSet):
    http_method_names = ['get','put']
    permission_classes = [IsRestuarantExist]

    def get_queryset(self):
        return Order.objects.all().filter(paid=True).filter(is_compelete=True)\
            .filter(restaurant_cart__restaurant__owner__user=self.request.user).filter(owner_approval=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRestaurantsOrderSerializer
        elif self.request.method == 'PUT':
            return OwnerApprovalOrdersSerializer
        else:
            return ShowRestaurantsOrderSerializer

    def update(self, request,pk):
        order = get_object_or_404(Order,pk=pk)
        serializer = OwnerApprovalOrdersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            approval = serializer.validated_data['owner_approval']
            order.owner_approval = approval
            order.save()
            if approval == True:
                message = f"Your order has been confirmed by the restaurant and will be delivered to you in {order.restaurant_cart.restaurant.delivery_time} minutes"
                payload = {
                    'username': '989116968310',
                    'password': 'E8Y!4',
                    'to': order.restaurant_cart.customer.user.phone_number,
                    'text': message
                }
                response = requests.post(url, data=payload)

                if response.status_code == 200:
                    return Response({"message": "Your message send successfully "},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"error": "unsend message"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"update successfully"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)









