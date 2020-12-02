from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    template = 'todo/signupuser.html'
    if request.method == 'GET':
        return render(request, template, {'form': UserCreationForm()})
    else:
        # Create a new user
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username,
                                                password=password1)
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(
                    request, 'todo/signupuser.html', {
                        'form':
                        UserCreationForm(),
                        'error':
                        'The username has already been taken. Please choose a new username'
                    })

        else:
            return render(request, template, {
                'form': UserCreationForm(),
                'error': 'Passwords did not match'
            })


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html',
                      {'form': AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(
                request, 'todo/loginuser.html', {
                    'form': AuthenticationForm(),
                    'error': 'Username and Password did not match'
                })


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')
