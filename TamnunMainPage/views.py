from django.shortcuts import render
from django.http import HttpResponse , JsonResponse



# Create your views here.
def general_calc_tamnun(request):
    return render(request, 'TamnunMainPage/calc_layout.html')

def dummy_data_serving(request):
        return JsonResponse({"itemA" : "A"})