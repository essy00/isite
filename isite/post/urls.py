from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    # path('contact', contact, name='contact'),
    path('', index, name='index'),
    path('detail/<str:slug>', detail, name='detail'),
    path('create/', create, name='create'),
    path('update/<str:slug>', update, name='update'),
    path('delete/<str:slug>', delete, name='delete'),
]
