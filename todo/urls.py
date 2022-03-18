from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    # ToDo
    path('current/', views.currenttodo, name='currenttodo'),
    path('create/', views.createtodo, name='createtodo'),
    path('todo/<str:slug>/', views.view_todo, name='view_todo'),
]
