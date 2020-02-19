from django.urls import path

from . import views

urlpatterns = [
    path('', views.general_calc_tamnun, name='calc'),

    path('json', views.dummy_data_serving, name = "dummy_data_serving") # For testing and dummy data serving 
]