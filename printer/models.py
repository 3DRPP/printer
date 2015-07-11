import uuid
import os
from datetime import datetime
import time
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

    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
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

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('printables', filename)

class Printable(models.Model):
    name = models.CharField('Object name', max_length=256, unique=True)
    filename = models.CharField(max_length=256)
    file = models.FileField(upload_to=get_file_path)
    date_added = models.DateTimeField(default=datetime.now)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    owner = models.ForeignKey(User)
    comment = models.TextField()

class Task(Printable, threading.Thread):
    def run(self):
        self.date_start = datetime.now()
        self.save()
        print("Printable started to be printed!")
        time.sleep(100)
        print("Printable has been printed!")
        self.date_end = datetime.now()
        self.save()
        printer = Printer()
        printer.state = 'PRTD'
        printer.current_task = None

    def is_waiting(self):
        return self.date_start == None

class Printer:
    STATES = (
        ('IDLE', 'Inactive'),
        ('PRTG', 'Printing'),
        ('PAUS', 'Pause'),
        ('INIT', 'Initializing'),
        ('PRTD', 'Printed')
    )
    __shared_state = {}
    current_task = None
    state = 'IDLE'
    def __init__(self):
        if self.__shared_state == {}:
            self.reset_position()
        self.__dict__ = self.__shared_state

    def start_task(self, task):
        if self.current_task is not None:
            print('Another task is already running.')
        if not task.is_waiting():
            print('This task is already launched or terminated.')
            return False

        self.current_task = task
        self.current_task.setDaemon(True)
        self.current_task.start()
        self.state = 'WARM'

    def reset_position(self):
        self.state = 'INIT'
        # Move axes to default position
        # Check for each switch
        # while (all switches are not closed):
        #   for stepper in steppers:
        #     if stepper.switch.is_open():
        #       rotate to start position
        time.sleep(10)
        self.state = 'IDLE'

    def auto_warming(self):
        # Launch a thread to handle temperature
        pass

    def stop_warming(self):
        # Stop thread if currently running
        pass

    def get_nozzle_temperature(self):
        return 250

    def start_ventilation(self):
        return

    def stop_ventilation(self):
        return