from django.urls import path, include
from . import views
from django.contrib.auth import views as password_views


app_name = 'myreels'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:type_no>/', views.detail, name='detail'),
    path('register', views.register, name='register'),
    path('login', views.auth_login, name='login'),
    path('logout', views.myLogout, name='logout'),
    path('search', views.search, name='search'),
    path('list', views.list, name='list'),
    path('cast/<int:cast_id>', views.cast_detail, name='cast_detail'),
    #path('placeorder/', views.placeorder, name='placeorder'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('password_reset/done', password_views.PasswordResetDoneView.as_view(template_name='myreels/forgot_password_done.html'), name='forgot_password_done'),
    path('reset/<uidb64>/<token>', password_views.PasswordResetConfirmView.as_view(template_name='myreels/forgot_password_confirm.html'), name='forgot_password_confirm'),
    path('view_orders', views.view_orders, name='view_orders'),
    # path('reset/done', password_views.PasswordResetCompleteView.as_view(template_name='myreels/password_reset_complete.html'), name='password_reset_complete'),
    #path('accounts/', include('django.contrib.auth.urls')),

    #path('placeorder/', views.placeorder, name='placeorder'),
]