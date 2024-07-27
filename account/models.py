from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
class MyUserManager(BaseUserManager):
    def create_user(self,name,last_name,phone_number,password=None,email=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError("Users must have an phone number")

        if not name:
            raise ValueError("Users must have name")

        if not last_name:
            raise ValueError("Users must have last_name")

        user = self.model(
            name=name,
            last_name=last_name,
            phone_number=phone_number,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name,last_name,phone_number,password=None,email=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name=name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^(\+98|0)?9\d{9}$',
                message="Phone number must be entered in the format  (\+98|0)?9\d{9}$"
            ),
        ],
    )
    name = models.CharField(max_length=255 ,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(default=True,blank=True)
    is_admin = models.BooleanField(default=False,blank=True)
    last_login = models.DateTimeField(blank=True,null=True)
    is_verified = models.BooleanField(default=False,blank=True)
    is_owner = models.BooleanField(default=False,blank=True)
    is_customer = models.BooleanField(default=False,blank=True)
    otp = models.CharField(max_length=6, blank=True)
    otp_expire_time = models.DateTimeField(blank=True, null=True)
    change_address_time = models.DateTimeField(blank=True,null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name","last_name"]
    objects = MyUserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin




class Customer(models.Model):
    user = models.OneToOneField('User',on_delete=models.CASCADE,related_name='customers',blank=True)
    address_name = models.CharField(max_length=200,blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.user.phone_number

class StoreType(models.Model):
    choice_list =[
        ('cofe','C'),
        ('restaurant','R')
    ]

    storetype_name = models.CharField(max_length=20,choices=choice_list,default='restaurant')
    storetype_desc = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.storetype_name

class Owner(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='owner',blank=True)
    stores_name = models.CharField(max_length=200)
    type = models.ForeignKey('StoreType',on_delete=models.PROTECT,related_name='owners')

    def __str__(self):
        return f"owner :{self.user.phone_number} for restaurant name : {self.stores_name}"


















