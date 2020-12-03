from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Todo
from .forms import TodoForm


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


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    context = {'todos': todos}
    return render(request, 'todo/currenttodos.html', context)


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user,
                                date_completed__isnull=False)
    context = {'todos': todos}
    return render(request, 'todo/completedtodos.html', context)


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {
                'form': TodoForm(),
                'error': 'Something went wrong'
            })


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {
                'todo': todo,
                'form': form,
                'error': 'Something went wrong'
            })

    return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
