from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    # ToDo
    path('current/', views.CurrentTodoList.as_view(), name='currenttodo'),
    path('completed/', views.completedtodo, name='completedtodo'),
    path('create/', views.CreateTodo.as_view(), name='createtodo'),
    path('todo/<str:slug>/', views.ViewTodo.as_view(), name='view_todo'),
    path('todo/<str:slug>/complete', views.complete_todo, name='complete_todo'),
    path('todo/<str:slug>/delete', views.delete_todo, name='delete_todo'),
]
