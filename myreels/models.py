from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.role

class Star(User):
    desc = models.TextField(blank=True)
    born_date = models.DateField(blank=True)
    city = models.CharField(blank=True, max_length=100)
    role = models.ManyToManyField(Role)

    class Meta:
        verbose_name = 'Star'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

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
    cast = models.ManyToManyField(Star)

    def __str__(self):
        return self.title




