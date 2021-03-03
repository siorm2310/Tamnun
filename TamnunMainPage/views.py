from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.generic import ListView
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import time
from .models import *
from .queries import ViewQueries
# import Algorithms.WBCalc as WBCalc


class PlatformSelectionView(ListView):
    """This view refers the user to a Platform selection list, divided by TMS

    Arguments:
        ListView {class} -- Django's class-based view
    """

    # view_types: {
    #     "UAV": UAVView,
    #     "Fighter": FighterView,
    #     "CargoAndHelos": CargoView,
    #     "HeavyCargo": HeavyCargoView,
    # }

    # TODO: edit this view
    model = AircraftType


def zik_view(request):
    context = {"a": 0, "b": 1}
    return render(request, "TamnunMainPage/zik_view.html", context=context)


def Weight_and_balance_api(request):
    pass


def general_calc_tamnun(request, methods=["POST", "GET"]):
    """
    TODO:
    1. get data relevant to the user from the data base
    2. arrange data to be delivered to the template
    3. render template with the data
    """

    return render(request, "TamnunMainPage/zik_view.html")


def display_main_page(request):
    """This view renders the Configuration builder view,
     based on the selected AircraftType selected in the PlatformSelectionView

    Arguments:
        request {WSGI request} -- Djagno's request object
        TMS     {string}       -- string representing the TMS, in XX-XX-XX format

    Returns:
        render                 -- renders the relevant ConfigBuilder view
    """
    context = ViewQueries.get_frontend_data(tms="11-11-11")
    return render(request, "TamnunMainPage/UAV.html", context)


@ensure_csrf_cookie
def calculation_endpoint(request):
    """This is an API endpoint. Activation of the endpoint with a POST request will trigger a configuraion sequence.

    Arguments:
        request {WSGI request} -- Djagno's request object. Must be a POST request and in JSON format,
        in accordance to agreed upon keys (See docs for example)

    Returns:
        CalcResult [JSON]      -- Result of calculation: Fuel limitations and centrograms
    """
    error_json = {
        "takeoff_fuel": "Error",
        "landing_fuel": "Error",
        "units": "Error",
        "centrogram": [],
    }
    if request.method == "POST":
        print("Got calculation request")
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as error:
            print(f"Error decoding client's request: {error}")
            return JsonResponse(error_json)
        except TypeError as error:
            print(f"Error in request format: {error}")
            return JsonResponse(error_json)
        time.sleep(2)
        print("done sleeping")
        print(data)
        CalcResult = json.dumps(WBCalc.get_limits(data))
        # return JsonResponse(CalcResult)
        return JsonResponse({"status": "Success"})
    return HttpResponse("No Calculation request was made")
