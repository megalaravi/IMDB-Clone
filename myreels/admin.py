from django.contrib import admin
from .models import Role, Cast, Category, Status, Movie, Order, Client

admin.site.register(Role)
admin.site.register(Category)
admin.site.register(Cast)
admin.site.register(Movie)
admin.site.register(Order)
admin.site.register(Client)
