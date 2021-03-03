from django.urls import path

from . import views

urlpatterns = [
    path("", views.zik_view, name="zik_view"),
]
