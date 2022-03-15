from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    # ToDo
    path('current/', views.currenttodo, name='currenttodo'),
    path('create/', views.createtodo, name='createtodo'),
]
