from django.shortcuts import render
from django.http import HttpResponse , JsonResponse, HttpRequest
import json
from .dummyData import dummyDataFile

# Create your views here.
def general_calc_tamnun(request, methods = ['POST', 'GET']):
    if request.method == 'POST':
        print('got request')
    return render(request, 'TamnunMainPage/UAV.html')

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
        print(json.loads(request.body))
        """TODO:
        1. Get the JSON
        2. Verify it is a JSON
        3. retrieve list of derivatives from JSON
        4. pass the list to the calculation
        """
    return JsonResponse(dummyDataFile.server_response)
        
