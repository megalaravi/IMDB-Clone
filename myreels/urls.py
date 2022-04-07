from django.urls import path
from . import views

app_name = 'myreels'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:type_no>/', views.detail, name='detail'),
    path('register', views.register, name='register'),
    path('login', views.auth_login, name='login'),
    path('logout', views.myLogout, name='logout'),
    path('search', views.search, name='search'),
    path('list', views.list, name='list'),
    #path('placeorder/', views.placeorder, name='placeorder'),
]