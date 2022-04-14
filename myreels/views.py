from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, SearchForm, OrderForm
from django.db.models.query_utils import Q
from django.http import HttpResponse
from .models import Movie, Status, Client, Cast, Order, User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError, EmailMessage
import logging

logger = logging.getLogger(__name__)

def index(request):
    top_rated = Movie.objects.exclude(status=Status.objects.get(status="Coming Soon")).order_by('-rating')[:7]
    coming_soon = Movie.objects.filter(status=Status.objects.get(status="Coming Soon"))
    return render(request, 'myreels/index.html', {'top_rated': top_rated, 'coming_soon': coming_soon})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registered Successfully')
            return redirect('myreels:index')
        messages.error(request, 'Not able to Register. Invalid information')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'myreels/register.html', context)

def detail(request, type_no):
    movie = Movie.objects.get(id=type_no)
    client = request.user
    #movieObj = Movies.objects.get(id=movieid)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                orders = Order.objects.filter(client=User.objects.get(username=request.user.username))

                flag = False

                if orders.exists():
                    for order in orders:
                        if order.movie.id == movie.id:
                            flag = True

                if flag == False:
                    order = Order()
                    #order = form.save(False)
                    order.movie = movie
                    order.client = client
                    order.save()
                    msg = 'Your order has been placed successfully.'
                else:
                    msg = 'You have already placed order for this movie'
                    return render(request, 'myreels/order_response.html', {'msg': msg})
            else:
                msg = 'Please login to the site to place the order'
                return render(request, 'myreels/not_logged_in.html', {'msg': msg})
        else:
            msg = 'Sorry '
        return render(request, 'myreels/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    context = {'form': form}
    return render(request, 'myreels/detail.html', {'details': movie})

def cast_detail(request, cast_id):
    cast = Cast.objects.get(id=cast_id)
    return render(request, 'myreels/cast_detail.html', {'cast': cast})

def list(request, results):
    #results = Movie.objects.filter(title__contains=title)
    return render(request, 'myreels/list.html', {'lists': results})

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # if request.session.keys():
            #     username = request.session['username']
            title = form.cleaned_data['title']
            results = Movie.objects.filter(title__contains=title)
            return render(request, 'myreels/list.html', {'lists': results})

    else:
        form = SearchForm()
    context = {'form': form}
    return render(request, 'myreels/search.html', context)


def auth_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, "Successfully logged in")
                request.session['username'] = username
                top_rated = Movie.objects.exclude(status=Status.objects.get(status="Coming Soon")).order_by('-rating')[
                            :7]
                coming_soon = Movie.objects.filter(status=Status.objects.get(status="Coming Soon"))
                return render(request, 'myreels/index.html', {'top_rated': top_rated, 'username': username, 'coming_soon': coming_soon})
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'myreels/login.html', context)

def myLogout(request):
    logout(request)
    # messages.info(request, "You have successfully Logged out.")
    # return redirect("myreels:index")
    try:
        del request.session['username']
    except:
        pass
    top_rated = Movie.objects.exclude(status=Status.objects.get(status="Coming Soon")).order_by('-rating')[
                :7]
    coming_soon = Movie.objects.filter(status=Status.objects.get(status="Coming Soon"))
    return render(request, 'myreels/index.html', {'top_rated': top_rated, 'coming_soon': coming_soon})

#def placeorder(request):


def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email_l = form.cleaned_data['email']
            logger.info('Email: %s', email_l)
            users = User.objects.filter(Q(email=email_l))
            user = get_object_or_404(User, email=email_l)
            #if users.exists():
            #for user in users:
            subject = "Reset your Reels Account Password"
            email_template = 'myreels/forgot_password_email.txt'
            content = {
                        "email": user.email,
                        "domain": '127.0.0.1:8000',
                        "site_name": 'Reels',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": 'http',
                    }
            email_content = render_to_string(email_template, content);
            try:
                final_email = EmailMessage(subject, email_content, to=[user.email])
                final_email.send()
                        #send_mail(subject, email_content, 'reels@gmail.com', [user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return redirect("myreels:forgot_password_done")
        else:
            logger.warning('Form is not valid')
    else:
        logger.warning('Form is not post')
    form = PasswordResetForm()
    context = {'form': form}
    return render(request, 'myreels/forgot_password.html', context)

def view_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(client=User.objects.get(username=request.user.username))
        return render(request, 'myreels/view_orders.html', {'orders': orders})
    else:
        return render(request, 'myreels/login.html', {})






# def formView(request):
#     if request.session.has_key('username'):
