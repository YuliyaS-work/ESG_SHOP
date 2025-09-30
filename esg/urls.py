from django.urls import path

from .views import *

urlpatterns = [
    path('', get_main_page, name='main'),
    path('catalog/', get_catalog, name='catalog'),
]
