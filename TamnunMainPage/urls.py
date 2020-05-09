from django.urls import path

from . import views

urlpatterns = [
    path("", views.display_main_page, name="UAV"),
    path(
        "Calc", views.calculation_endpoint, name="CalcEndpoint"
    ),  # recieves data from frontEnd
    path("hello", views.display_main_page, name="hello"),  # recieves data from frontEnd
    path(
        "PlatformSelect/", views.PlatformSelectionView.as_view(), name="hello"
    ),  # recieves data from frontEnd
]
