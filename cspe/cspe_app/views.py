from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    car_details = CarDetails.objects.all()
    if request.method=="POST":
        car_age = request.POST['car_age']
        km_driven = request.POST['km_driven']
        mileage = request.POST['mileage']
        horsepower = request.POST['horsepower']
        
        ins = CarDetails(car_age=car_age, km_driven=km_driven, mileage=mileage, horsepower=horsepower)
        ins.save()

    return render(request, 'home.html', {'car_details':car_details})

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    return render(request, 'contactus.html')