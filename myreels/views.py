from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, SearchForm
from django.http import HttpResponse
from .models import Movie, Status

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
    details = Movie.objects.get(id=type_no)
    return render(request, 'myreels/detail.html', {'details': details})

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
    # logout(request)
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

# def formView(request):
#     if request.session.has_key('username'):
