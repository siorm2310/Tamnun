from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.
def general_calc_tamnun(request):
    return render(request, 'TamnunMainPage/calc_layout.html')