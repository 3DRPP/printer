from datetime import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
import threading


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(name=name, email=email)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    name = models.CharField('user name', max_length=254, unique=True)
    email = models.EmailField('email address', max_length=254, unique=True)
    pushbullet_api_key = models.TextField(null=True)
    send_emails = models.BooleanField(default=False)
    send_pushbullets = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.now)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            # Do more things here
        else:
            super().save(*args, **kwargs)

    def switch_emails(self):
        self.send_emails = not self.send_emails
        self.save()

    def switch_pushbullets(self):
        if self.pushbullet_api_key:
            self.send_pushbullets = not self.send_pushbullets
            self.save()

class Printable(models.Model, threading.Thread):
    name = models.CharField('Object name', max_length=256, unique=True)
    file = models.FileField(upload_to='printables')
    date_added = models.DateTimeField(default=datetime.now)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    owner = models.ForeignKey(User)

    def run(self):
        print("test")
