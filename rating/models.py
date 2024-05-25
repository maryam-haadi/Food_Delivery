from django.db import models
from account.models import User
from core.models import Food
# Create your models here.

class Rating(models.Model):
    food = models.ForeignKey('core.Food',on_delete=models.CASCADE,related_name='ratings')
    user = models.ForeignKey('account.User',on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(choices=((1,'1Stars'),(2,'2Stars'),(3,'3Stars'),(4,'4Stars'),(5,'5Stars')))

    class Meta:
        unique_together=('food','user')

    def __str__(self):
        return f"{self.user.phone_number} rated {self.food.name} - {self.stars} stars"



class RestaurantRating(models.Model):
    restaurant = models.ForeignKey('core.Restaurant',on_delete=models.CASCADE,related_name='ratings')
    user = models.ForeignKey('account.User',on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(choices=((1,'1Stars'),(2,'2Stars'),(3,'3Stars'),(4,'4Stars'),(5,'5Stars')))

    class Meta:
        unique_together=('restaurant','user')

    def __str__(self):
        return f"{self.user.phone_number} rated {self.restaurant.name} - {self.stars} stars"















