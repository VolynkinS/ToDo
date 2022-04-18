from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView

from .forms import TodoForm, UserRegisterFrom, UserLoginFrom
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


@login_required
def currenttodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodo.html', {'todos': todos})


class ViewTodo(UpdateView, LoginRequiredMixin):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/view_todo.html'
    success_url = '/current/'


class CreateTodo(CreateView, LoginRequiredMixin):
    form_class = TodoForm
    template_name = 'todo/createtodo.html'
    success_url = '/current/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


@login_required
def completedtodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'todo/completedtodo.html', {'todos': todos})


@login_required
def complete_todo(request, slug):
    todo = get_object_or_404(Todo, slug=slug, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('todo:currenttodo')


@login_required
def delete_todo(request, slug):
    todo = get_object_or_404(Todo, slug=slug, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo:currenttodo')


def signupuser(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo:currenttodo')
    else:
        form = UserRegisterFrom()
    return render(request, 'todo/signupuser.html', {'form': form})


def loginuser(request):
    if request.method == 'POST':
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            # The same as authenticate(request, **request.POST)
            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('todo:currenttodo')
    else:
        form = UserLoginFrom()
    return render(request, 'todo/loginuser.html', {'form': form})


@login_required
def logoutuser(request):
    logout(request)
    return redirect('todo:home')
