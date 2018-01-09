from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Book(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    balance = models.FloatField(default=0)


class Lease(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_start = models.DateTimeField(default=timezone.now)
    date_finish = models.DateTimeField()
    value = models.FloatField()
    balance = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return '{} {} {} {}'.format(self.book.name, self.user.username, self.balance, self.active)

    @property
    def active(self):
        if (self.date_finish > timezone.now()) and (self.date_start <= timezone.now()):
            return True
        else:
            return False

    @property
    def balance(self):
        if self.active:
            return (self.date_finish - timezone.now()).days
        else:
            return 0
