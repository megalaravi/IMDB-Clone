from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Client(User):
    phoneNo = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name='Client'

class Role(models.Model):
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.role

class Cast(models.Model):
    name = models.CharField(max_length=100, default="")
    desc = models.TextField(blank=True)
    born_date = models.DateField(blank=True)
    city = models.CharField(blank=True, max_length=100)
    role = models.ManyToManyField(Role)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.name

class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class Status(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status

class Movie(models.Model):
    LANGUAGE_CHOICES = [
        ('english', 'ENGLISH'),
        ('german', 'GERMAN'),
        ('french', 'FRENCH'),
    ]
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='media')
    banner = models.ImageField(upload_to='media')
    category = models.ManyToManyField(Category)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=10)
    status = models.ManyToManyField(Status)
    year = models.DateField()
    rating = models.DecimalField(max_digits=10,decimal_places=1, blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    cast = models.ManyToManyField(Cast)

    def __str__(self):
        return self.title


class Order(models.Model):
    movie = models.ForeignKey(Movie, related_name='orderItems', on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name='clientOrderedItems', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.movie.title + " ordered by " + self.client.username





