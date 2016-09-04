from django.conf.urls import url
from django.contrib import admin
from . import views


app_name = 'interface'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/', views.submission, name='submission'),
    url(r'^thanks/', views.thanks, name='thanks'),
]
