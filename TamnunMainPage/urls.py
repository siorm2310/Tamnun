from django.urls import path

from . import views

urlpatterns = [
    path('', views.general_calc_tamnun, name='calc'),
]