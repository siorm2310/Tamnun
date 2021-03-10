from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.generic import ListView
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import time
from .models import *
from .queries import ViewQueries
# import Algorithms.WBCalc as WBCalc


def zik_view(request):
    context = {"a": 0, "b": 1}
    with open("TamnunMainPage\ZikDemo\data.json", 'r') as datafile:
        data = json.loads(datafile.read(), encoding="utf-8")
    return render(request, "TamnunMainPage/zik_view.html", context=data)


def display_main_page(request):
    """This view renders the Configuration builder view,
     based on the selected AircraftType selected in the PlatformSelectionView
x`
    Arguments:
        request {WSGI request} -- Djagno's request object
        TMS     {string}       -- string representing the TMS, in XX-XX-XX format

    Returns:
        render                 -- renders the relevant ConfigBuilder view
    """
    context = ViewQueries.get_frontend_data(tms="11-11-11")
    return render(request, "TamnunMainPage/UAV.html", context)
