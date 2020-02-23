from django.shortcuts import render
from django.http import HttpResponse , JsonResponse, HttpRequest



# Create your views here.
def general_calc_tamnun(request):
    return render(request, 'TamnunMainPage/calc_layout.html')

def dummy_data_serving(request):
        return JsonResponse({"itemA" : "A"})

def recieve_frontend_data(request):
    # TODO: figure out a way to handle posting of JSON from the front end
    
    if request.method == 'POST':
        """TODO:
        1. Get the JSON
        2. Verify it is a JSON
        3. retrieve list of derivatives from JSON
        4. pass the list to the calculation
        """
        pass
        