from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def general_calc_tamnun(request):
    return render(request, 'TamnunMainPage/calc_layout.html')