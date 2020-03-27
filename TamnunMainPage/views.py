from django.shortcuts import render
from django.http import HttpResponse , JsonResponse, HttpRequest
import json, time
from .models import *

# Create your views here.
def general_calc_tamnun(request, methods = ['POST', 'GET']):
    """
    TODO:
    1. get data relevant to the user from the data base
    2. arrange data to be delivered to the template
    3. render template with the data
    """

    return render(request, 'TamnunMainPage/UAV.html')

def display_main_page(request, chosen_aircraft_tms):
    try:
        aircraftType = AircraftType.objects.get(TMS = chosen_aircraft_tms)
        aircrafts = Aircraft.objects.filter(aircraftType = aircraftType)
        items = Item.objects.filter(relatedAircraft = aircraftType)
        fuelFlows = FuelFlow.objects.filter(aircraftType = aircraftType)
        envelopes = Envelope.objects.filter(aircraftType = aircraftType)

    except expression as identifier:
        pass

    delivery_data = {
        "aircraftType" : aircraftType,
        "aircrafts" : aircrafts,
        "items" : items,
        "fuelFlows" : fuelFlows,
        "envelopes" : envelopes
    }
    return render(request, delivery_data)

def dummy_data_serving(request):
        return JsonResponse({
            "items" : 
            [{
                "פריט 1" : "A",
                "פריט 2" : "B",
                "פריט 3" : "C"
            }],

            "tailNumbers" : 
            [{
                "315" : "A",
                "654" : "B",
                "342" : "C",
            }],
        }
        )

def recieve_frontend_data(request):  
    if request.method == 'POST':
        print('got a request')
        # print(json.loads(request.body))
        time.sleep(2)
        print('done sleeping')
        """TODO:
        1. Get the JSON
        2. Verify it is a JSON
        3. retrieve list of derivatives from JSON
        4. pass the list to the calculation
        """
        return JsonResponse({"shloops" : "gloops"})

# def process_calculation_requests(request):
#     if request.method == 'POST':
#         selections = request.body
#         solutions = calculate_WB_limits(selections)
#     return(solution)