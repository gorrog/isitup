from django.conf.urls import url
from django.contrib import admin
from . import views


app_name = 'interface'
urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    url(r'^submit/', views.submission, name='submission'),
    url(r'^thanks/', views.thanks, name='thanks'),
    
    # going through the questions details
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail,
# name='detail'),
    # going through the questions results
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results,
# name='results'),
]
