from django.contrib import admin
from .models import Role, Star, Category, Status, Movie

admin.site.register(Role)
admin.site.register(Star)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Movie)
