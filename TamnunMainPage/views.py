from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.generic import ListView
from django.views.decorators.csrf import ensure_csrf_cookie
import json, time
from .models import *
from .queries import ViewQueries

from .Algorithms import WBCalc


class PlatformSelectionView(ListView):
    """This view refers the user to a Platform selection list, divided by TMS

    Arguments:
        ListView {class} -- Django's class-based view
    """

    # TODO: edit this view
    model = AircraftType


def general_calc_tamnun(request, methods=["POST", "GET"]):
    """
    TODO:
    1. get data relevant to the user from the data base
    2. arrange data to be delivered to the template
    3. render template with the data
    """

    return render(request, "TamnunMainPage/UAV.html")


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
    if request.method == "POST":
        print("Got calculation request")
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as error:
            print(f"Error decoding client's request: {error}")
            return JsonResponse(
                {
                    "takeoff_fuel": "Error",
                    "landing_fuel": "Error",
                    "units": "Error",
                    "centrogram": [],
                }
            )
        except TypeError as error:
            print(f"Error in request format: {error}")
            return JsonResponse(
                {
                    "takeoff_fuel": "Error",
                    "landing_fuel": "Error",
                    "units": "Error",
                    "centrogram": [],
                }
            )
        time.sleep(2)
        print("done sleeping")
        print(data)
        CalcResult = json.dumps(WBCalc.get_limits(data))
        # return JsonResponse(CalcResult)
        return JsonResponse({"status": "Success"})
    return HttpResponse("No Calculation request was made")
