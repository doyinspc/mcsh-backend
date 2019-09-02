from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .managers import UserManager, ClientManager, EmployeeManager
from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    password = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_permission = models.PositiveIntegerField(default=1   )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
 
    def __str__(self):
        return self.email


class Client(User, PermissionsMixin):
    fullname = models.CharField(_('name'), max_length=120, blank=False)
    cardno = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True )
    gender = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone']

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')

class Category(models.Model):
    name = models.CharField(max_length=100, default='None')
    is_active = models.BooleanField(_('active'), default=False)

class Employee(User, PermissionsMixin):
    fullname = models.CharField(_('fullname'), max_length=120, blank=True)
    profile = models.CharField(_('about'), max_length=1000, blank=True)
    photo = models.ImageField(upload_to='photo', null=True, blank=True)
    empno = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.PositiveIntegerField(default=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone']

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    bempno = models.ForeignKey(Employee, related_name="%(app_label)s_%(class)s_emp", related_query_name="%(app_label)s_%(class)ss",  on_delete=models.CASCADE)
    bcardno = models.ForeignKey(Client,  related_name="%(app_label)s_%(class)s_card", related_query_name="%(app_label)s_%(class)ss", on_delete=models.CASCADE)
    comment = models.CharField(_('comment'), max_length=1000, blank=True)
    is_booked = models.BooleanField(_('active'), default=False)
    is_paid = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=1)
    date_booked = models.DateField(_('date booked'), auto_now=False, auto_now_add=False)
    time_booked = models.TimeField(_('time booked'), auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(_('date joined'), auto_now_add=True)



