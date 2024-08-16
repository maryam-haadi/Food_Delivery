from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import mixins
from .serializers import *
from .models import *
from customer.permissions import *
from rest_framework.decorators import action
from core.serializers import *
from account.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rating.models import *
from rating.serializers import *
from .serializers import *
import requests
# Create your views here.





# class CartItemViewset(ModelViewSet):
#     permission_classes = [IsCustomer]
#     http_method_names = ['post','get','put']
#
#     def get_queryset(self):
#         return Restaurant_cart_item.objects.all().filter(restaurant_cart__customer__user = self.request.user)
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return Addcartitemserializer
#         elif self.request.method == 'GET':
#             return Showcartitemserializer
#         else:
#             return Updatecartitemserializer
#
#
#     def create(self, request, *args, **kwargs):
#         serializer = Addcartitemserializer(data = request.data)
#         if serializer.is_valid(raise_exception=True):
#             food_id = serializer.validated_data['food']['pk']
#             food = get_object_or_404(Food,id=food_id)
#             restaurant = food.menu.restaurant
#             user = request.user
#             customer = get_object_or_404(Customer,user=user)
#
#             restaurant_cart,created = Restaurant_cart.objects.get_or_create(customer=customer,restaurant=restaurant)
#             if created:
#                 restaurant_cart_item = Restaurant_cart_item.objects.create(restaurant_cart=restaurant_cart,food=food)
#                 return Response({"message":"created succsesfully","data":serializer.data},status=status.HTTP_201_CREATED)
#
#             else:
#                 if Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first() is None:
#                     restaurant_cart_item = Restaurant_cart_item.objects.create(restaurant_cart=restaurant_cart,food=food)
#                     return Response({"message":"created succsesfully","data":serializer.data},status=status.HTTP_201_CREATED)
#                 else:
#                     item = Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first()
#                     item.quantity += 1
#                     item.save()
#
#                     return Response({"message": "quantity of food plus one"},status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#
#     def update(self, request, pk):
#         instance = get_object_or_404(Restaurant_cart_item,pk=pk)
#         serializer = Updatecartitemserializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             quantity = serializer.validated_data['quantity']
#             if quantity == 0:
#                 instance.delete()
#                 cart = instance.restaurant_cart
#                 if Restaurant_cart_item.objects.all().filter(restaurant_cart=cart).first() is None:
#                     cart.delete()
#                     order = Order.objects.all().filter(restaurant_cart=cart).filter(restaurant_cart__customer__user=request.user).first()
#                     if order is not None:
#                         order.delete()
#                 return Response({"message":"remove this cart item from your cart"},status=status.HTTP_200_OK)
#             else:
#                 instance.quantity = quantity
#                 instance.save()
#                 return Response({"message": "update quantity of your cartitem"}, status=status.HTTP_200_OK)
#
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class CartViewset(ModelViewSet):
    permission_classes = [IsCustomer]
    http_method_names = ['get','delete','post']

    def get_distance(self,user_lat, user_long, res_lat, res_long):

        earth_radius = 6371

        user_lat = radians(user_lat)
        user_long = radians(user_long)
        restaurant_lat = radians(res_lat)
        restaurant_long = radians(res_long)
        dlon = restaurant_long - user_long
        dlat = restaurant_lat - user_lat
        a = sin(dlat / 2) * sin(dlat / 2) + cos(user_lat) * cos(restaurant_lat) * sin(dlon / 2) * sin(dlon / 2)
        c = 2 * asin(sqrt(a))
        distance = earth_radius * c
        return distance



    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartShowSerializer
        else:
            return CartPostSerializer

    def get_queryset(self):
        return Restaurant_cart.objects.all().filter(customer__user=self.request.user).filter(is_compelete=False)

    def create(self, request, *args, **kwargs):
        serializer = CartPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            res_id = serializer.validated_data['restaurant']['id']
            restaurant = get_object_or_404(Restaurant,id=res_id)
            customer = get_object_or_404(Customer,user=request.user)
            if Restaurant_cart.objects.all().filter(customer=customer).filter(restaurant=restaurant).filter(is_compelete=False).first() is None:
                if customer.address_name is None or customer.latitude is None or customer.longitude is None:
                    return Response({"error message":"Please select your address first"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    dist = self.get_distance(customer.longitude,customer.longitude,restaurant.latitude,restaurant.longitude)
                    if dist > 5000:
                        return Response({"message":"This restaurant is not within your address range"},status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if (datetime.now().time() < restaurant.close_time and datetime.now().time() > restaurant.open_time) or restaurant.is_open==True:
                            cart = Restaurant_cart.objects.create(customer=customer,restaurant=restaurant)
                            return Response({"message":"this cart created successfully"},status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message":"The restaurant is closed"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"this cart already exist"})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def __delete__(self, instance):
        instance.delete()
        order = Order.objects.all().filter(restaurant_cart=instance)\
            .filter(restaurant_cart__customer__user=self.request.user).first()
        if order is not None:
            order.delete()
        return Response({"message":"delete cart secsessfully"},status=status.HTTP_204_NO_CONTENT)





class CartItemNestedViewset(ModelViewSet):
    permission_classes = [IsCustomer]
    http_method_names = ['post','get','put']

    def get_queryset(self):
        return Restaurant_cart_item.objects.all().filter(restaurant_cart__customer__user = self.request.user).filter(restaurant_cart_id=self.kwargs['cart_pk'])\
            .filter(restaurant_cart__is_compelete=False)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Addcartitemserializer
        elif self.request.method == 'GET':
            return Showcartitemserializer
        else:
            return Updatecartitemserializer


    def create(self, request, *args, **kwargs):
        serializer = Addcartitemserializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            food_id = serializer.validated_data['food']['pk']
            food = get_object_or_404(Food,id=food_id)
            restaurant_cart = get_object_or_404(Restaurant_cart,pk=self.kwargs['cart_pk'])
            restaurant = restaurant_cart.restaurant
            user = request.user
            customer = get_object_or_404(Customer,user=user)


            foods = Food.objects.all().filter(menu__restaurant=restaurant)
            if food in foods:
                if Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first() is None:
                    restaurant_cart_item = Restaurant_cart_item.objects.create(restaurant_cart=restaurant_cart,food=food)
                    return Response({"message":"created succsesfully","data":serializer.data},status=status.HTTP_201_CREATED)
                else:
                    item = Restaurant_cart_item.objects.all().filter(restaurant_cart=restaurant_cart).filter(food=food).first()
                    item.quantity += 1
                    item.save()

                    return Response({"message": "quantity of food plus one"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Please note that this food is not available in this restaurant"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




    def update(self,request,pk,**kwargs):
        instance = get_object_or_404(Restaurant_cart_item,pk=pk)
        serializer = Updatecartitemserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            quantity = serializer.validated_data['quantity']
            if quantity == 0:
                instance.delete()
                cart = instance.restaurant_cart
                if Restaurant_cart_item.objects.all().filter(restaurant_cart=cart).first() is None:
                    cart.delete()
                    order = Order.objects.all().filter(restaurant_cart=cart).filter(restaurant_cart__customer__user=request.user).first()
                    if order is not None:
                        order.delete()

                return Response({"message":"remove this cart item from your cart"},status=status.HTTP_200_OK)
            else:
                instance.quantity = quantity
                instance.save()
                return Response({"message": "update quantity of your cartitem"}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class OrderViewset(ModelViewSet):
    def get_distance(self,user_lat, user_long, res_lat, res_long):

        earth_radius = 6371

        user_lat = radians(user_lat)
        user_long = radians(user_long)
        restaurant_lat = radians(res_lat)
        restaurant_long = radians(res_long)
        dlon = restaurant_long - user_long
        dlat = restaurant_lat - user_lat
        a = sin(dlat / 2) * sin(dlat / 2) + cos(user_lat) * cos(restaurant_lat) * sin(dlon / 2) * sin(dlon / 2)
        c = 2 * asin(sqrt(a))
        distance = earth_radius * c
        return distance


    http_method_names = ['get','put']
    permission_classes = [IsCustomer]

    def get_serializer_context(self):
        res_cart = get_object_or_404(Restaurant_cart,pk=self.kwargs['cart_pk'])

        return {"min_price":res_cart.restaurant.min_cart_price}

    def get_queryset(self):

            return Order.objects.filter(restaurant_cart=self.kwargs['cart_pk'])\
                .filter(restaurant_cart__customer__user=self.request.user).filter(paid=False)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowOrderSerializer
        else:
            return UpdateOrderAddressSerializer



    def update(self, request,pk,**kwargs):
        order = get_object_or_404(Order,pk=pk)
        serializer = UpdateOrderAddressSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant_cart_pk = self.kwargs['cart_pk']
            res_cart = get_object_or_404(Restaurant_cart,pk=restaurant_cart_pk)
            restaurant = res_cart.restaurant
            customer_lat = serializer.validated_data['latitude']
            customer_long = serializer.validated_data['longitude']

            dist = self.get_distance(customer_lat,customer_long,restaurant.latitude,restaurant.longitude)
            print("distance",dist)
            if dist > 5000:
                return Response({"message":"Your selected address is outside the restaurant area"},status=status.HTTP_400_BAD_REQUEST)
            else:
                order.delivery_address_name = serializer.validated_data['delivery_address_name']
                order.latitude = customer_lat
                order.longitude = customer_long
                order.save()
                return Response({"message":"updated address sucssesfully","data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



    def list(self, request, *args, **kwargs):

        if Order.objects.filter(restaurant_cart=self.kwargs['cart_pk']).filter(restaurant_cart__customer__user=self.request.user).first() is None:
            id = self.kwargs['cart_pk']
            restaurant_cart = get_object_or_404(Restaurant_cart,id=id)
            cart_items = Restaurant_cart_item.objects.all().filter(restaurant_cart_id=id)
            min_price =restaurant_cart.restaurant.min_cart_price
            total = 0
            for item in cart_items:
                total+=item.quantity * item.food.price

            if total < min_price:
                return Response({"message":f"Your minimum purchase must {min_price}"},status=status.HTTP_400_BAD_REQUEST)
            else:
                customer = Customer.objects.all().filter(user=self.request.user).first()
                order = Order.objects.create(restaurant_cart_id=self.kwargs['cart_pk'],
                                             delivery_address_name=customer.address_name,
                                             latitude=customer.latitude,
                                             longitude=customer.longitude)

                serializer = ShowOrderSerializer(instance=order,many=False)
                return Response({"message":"order for you","data":serializer.data},status=status.HTTP_201_CREATED)
        else:
            order = Order.objects.filter(restaurant_cart=self.kwargs['cart_pk'])\
                .filter(restaurant_cart__customer__user=self.request.user).first()

            total_price = order.total_price
            delivery_price = order.restaurant_cart.restaurant.delivery_price
            total_order = total_price - delivery_price
            if total_order < order.restaurant_cart.restaurant.min_cart_price:
                return Response({"message":f"Your minimum purchase must {order.restaurant_cart.restaurant.min_cart_price}"},status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ShowOrderSerializer(instance=order,many=False)
                return Response({"data":serializer.data},status=status.HTTP_200_OK)


def get_verification_code():
    # Upper caset letters to select from
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_letters = ""
    # Generate 5 Random Uppercase letters
    for i in range(5):
        random_check = random.randint(0, 1)
        if random_check == 0:
            random_letter = random.choice(uppercase_letters)
            random_letters += random_letter
        else:
            random_number = random.randint(0, 9)
            random_letters += str(random_number)

    return random_letters



def get_daynamic_password():
    random_letters = ""
    # Generate 5 Random Uppercase letters
    for i in range(5):
        random_number = random.randint(0, 9)
        random_letters += str(random_number)

    return random_letters




url = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
class CreatePaymentViewSet(GenericViewSet,mixins.CreateModelMixin):
    http_method_names = ['post']
    permission_classes = [IsCustomer]
    serializer_class = CreatePaymentSerializer

    def get_queryset(self):
        return Payment.objects.all().filter(order__restaurant_cart__customer__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreatePaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_id = serializer.validated_data['order']['id']
            origin_card_number = serializer.validated_data['origin_card_number']
            cvv2 = serializer.validated_data['cvv2']
            order = get_object_or_404(Order,id=order_id)

            if Payment.objects.filter(order=order).filter(origin_card_number=origin_card_number).\
                filter(cvv2=cvv2).first() is None:
                payment = Payment.objects.create(order=order,origin_card_number=origin_card_number,
                                                cvv2=cvv2)

                verification = get_verification_code()
                payment.verification = verification
                payment.expire_time = timezone.now() + timedelta(minutes=3)
                daynamic_password = get_daynamic_password()
                payment.daynamic_password = daynamic_password
                payment.save()
                print("daynamic_password :",daynamic_password)

                message = f"your daynamic password for payment id {payment.id} is : {daynamic_password}"
                payload = {
                    'username': '989116968310',
                    'password': 'E8Y!4',
                    'to': payment.order.restaurant_cart.customer.user.phone_number,
                    'text': message
                }
                response = requests.post(url, data=payload)

                if response.status_code == 200:
                    return Response({"message1":"verification code for your payment","verification":verification,"message2":"daynamic password send seccsesfully"},status=status.HTTP_201_CREATED)
                else:
                    return Response({"error":"daynamic password unsend"},status=status.HTTP_400_BAD_REQUEST)
            else:
                payment = Payment.objects.filter(order_id=order_id).filter(origin_card_number=origin_card_number).\
                filter(cvv2=cvv2).first()

                verification = get_verification_code()
                payment.verification = verification
                payment.expire_time = timezone.now() + timedelta(minutes=3)
                daynamic_password = get_daynamic_password()
                payment.daynamic_password = daynamic_password
                payment.save()
                print("daynamic_password :", daynamic_password)

                message = f"your daynamic password for payment id {payment.id} is : {daynamic_password}"
                payload = {
                    'username': '989116968310',
                    'password': 'E8Y!4',
                    'to': payment.order.restaurant_cart.customer.user.phone_number,
                    'text': message
                }
                response = requests.post(url, data=payload)

                if response.status_code == 200:
                    return Response({"message":"verification code for your payment","verification":verification,"message2":"daynamic password send seccsesfully"},status=status.HTTP_200_OK)
                else:
                    return Response({"error":"daynamic password unsend"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class VerifyPaymentViewSet(ModelViewSet):
    http_method_names = ['post']
    permission_classes = [IsCustomer]
    serializer_class = VerifyPaymentSerializer

    def get_queryset(self):
        return Payment.objects.all().filter(order__restaurant_cart__customer__user = self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = VerifyPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_id = serializer.validated_data['order']['id']
            origin_card_number = serializer.validated_data['origin_card_number']
            cvv2 = serializer.validated_data['cvv2']
            daynamic_password = serializer.validated_data['daynamic_password']
            verification = serializer.validated_data['verification']
            order = get_object_or_404(Order,id=order_id)
            payment = Payment.objects.all().filter(order=order).filter(origin_card_number=origin_card_number).\
                filter(cvv2=cvv2).first()
            if payment is not None and payment.is_complete == False:
                if payment.verification==verification and payment.daynamic_password==daynamic_password\
                     and payment.expire_time is not None and payment.expire_time > timezone.now():
                     payment.is_complete = True
                     payment.order.paid = True
                     payment.order.is_compelete = True
                     payment.order.restaurant_cart.is_compelete = True
                     payment.order.restaurant_cart.save()
                     payment.order.save()
                     payment.save()

                     message = f"You have an order from the customer with phone number  {payment.order.restaurant_cart.customer.user.phone_number}"
                     payload = {
                         'username': '989116968310',
                         'password': 'E8Y!4',
                         'to': payment.order.restaurant_cart.restaurant.owner.user.phone_number,
                         'text': message
                     }
                     response = requests.post(url, data=payload)

                     if response.status_code == 200:
                         return Response({"message": "Your payment has been successfully completed"},
                                         status=status.HTTP_200_OK)
                     else:
                         return Response({"error": "unsend message"}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"message":"your payment verification incorrect"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"not exist any payment"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)















































