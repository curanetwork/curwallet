"""Base models"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.mail import send_mail
from django_extensions.db.fields import RandomCharField

from .conf import settings as sett

import uuid


class Transaction(models.Model):
    CURRENCIES = (
        (sett.ICO_TOKEN_SYMBOL.upper(), sett.ICO_TOKEN_SYMBOL.upper()),
        ('USD', 'USD')
    )
    for currency in sett.ICO_CURRENCIES:
        CURRENCIES = CURRENCIES + ((currency[0].upper(), currency[0].upper()),)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE)
    currency = models.CharField(choices=CURRENCIES, max_length=20)
    code = models.CharField(max_length=200)
    amount = models.FloatField(null=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, default="pending")
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}{self.currency} ({self.description})"


class Referral(models.Model):
    referred = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    related_name="log_referrer",
                                    on_delete=models.CASCADE)
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name="log_referrals",
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('You must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        from web3 import Web3
        from base import helpers

        wallet = helpers.create_account(user.password)
        user.address = wallet.address
        user.private_key = Web3.toHex(wallet.privateKey)

        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    affiliate_id = RandomCharField(length=8, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='referrals',
        on_delete=models.CASCADE
    )
    social_url = models.URLField(max_length=1000)
    review = models.TextField()
    mobile_no = models.CharField(max_length=50)
    address = models.CharField(max_length=42)
    private_key = models.CharField(max_length=66)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'date_joined']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
