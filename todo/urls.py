from django.urls import path

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
]
