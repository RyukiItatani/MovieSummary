from django.urls import path
from polls import views

app_name="polls"
urlpatterns = [
    path('index', views.Index, name='index'),
    path('', views.Index, name='index')
]