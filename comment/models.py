from django.db import models
from account.models import User
from core.models import Food
# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey('account.User',on_delete=models.CASCADE)
    food = models.ForeignKey('core.Food',on_delete=models.CASCADE,related_name='comments')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='replies',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone_number


class CommentRestaurant(models.Model):
    text = models.TextField()
    user = models.ForeignKey('account.User',on_delete=models.CASCADE)
    restaurant = models.ForeignKey('core.Restaurant',on_delete=models.CASCADE,related_name='comments')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='replies',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone_number
























