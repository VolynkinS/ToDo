from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView

from .forms import TodoForm, UserRegisterForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


class CurrentTodoList(LoginRequiredMixin, ListView):
    model = Todo
    # template_name = 'todo/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user,
                                   datecompleted__isnull=True)


class CompleteTodoList(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = 'todos'
    template_name = 'todo/completedtodo.html'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user,
                                   datecompleted__isnull=False)


class ViewTodo(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/view_todo.html'
    success_url = '/current/'


class CreateTodo(LoginRequiredMixin, CreateView):
    form_class = TodoForm
    template_name = 'todo/createtodo.html'
    success_url = '/current/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo:currenttodo')
    else:
        form = UserRegisterForm()
    return render(request, 'todo/signupuser.html', {'form': form})
