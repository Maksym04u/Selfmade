from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('User must have a password')
        

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.save()
        return user
    

class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class MyUser(AbstractUser):
    password = models.CharField()
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    description = models.TextField(max_length=750, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    links = models.CharField(blank=True)
    interests = models.ManyToManyField(Interest, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "password"]

    def __str__(self):
        return self.username
    



