from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

def home(request):
    

    return render(request, 'home.html')

def result(request):
    context={}
    car_details = CarDetails.objects.all()
    if request.method=="POST":
        car_age = request.POST['car_age']
        km_driven = request.POST['km_driven']
        mileage = request.POST['mileage']
        horsepower = request.POST['horsepower']
        engine = request.POST['engine']
        seats = request.POST['seats']
        fuel_type = request.POST['fuel_type']
        transmission_type = request.POST.get('transmission_type')
        structural_damage = request.POST['structural_damage']
        
        
        
    context['car_age'] = car_age
    context['km_driven'] = km_driven
    context['mileage'] = mileage
    context['horsepower'] = horsepower
    context['engine']= engine  
    context['seats']= seats    
    context['fuel_type']= fuel_type    
    context['transmission_type']= transmission_type
    context['structural_damage']= structural_damage

    df = pd.read_csv("E:\SE\Sem 4\Mini-Project\MiniProjectSem4\cspe\cspe_app\car_v4.csv")

    df["mileage_modifier"]=0
    df.loc[(df['mileage']<=30),"mileage_modifier"]=0.05
    df.loc[(df['mileage']<=20),"mileage_modifier"]=0.1
    df.loc[(df['mileage']<=10),"mileage_modifier"]=0.15
    df.loc[(df.Structural_damage=="none"), 'selling_price'] = df.selling_price
    df.loc[(df.Structural_damage=="low"), 'selling_price'] = df.selling_price - df.selling_price*0.25*df.mileage_modifier
    df.loc[(df.Structural_damage=="moderate"), 'selling_price'] = df.selling_price - df.selling_price*0.5*df.mileage_modifier

    inputs = df.drop(['selling_price','id','car_name','brand','model','new_price','min_cost_price','max_cost_price','seller_type','mileage_modifier'],axis='columns')
    target = df['selling_price']

    def dummies(x,df):
        temp = pd.get_dummies(df[x], drop_first = True)
        df = pd.concat([df, temp], axis = 1)
        df.drop([x], axis = 1, inplace = True)
        return df

    inputs=dummies('fuel_type',inputs)
    inputs=dummies('transmission_type',inputs)
    inputs=dummies('Structural_damage',inputs)

    x_train,x_test,y_train,y_test = train_test_split(inputs,target,test_size=0.1)

    model = RandomForestRegressor(max_features='sqrt',bootstrap='True')
    model.fit(x_train,y_train)

    var1 = float(car_age)
    var2 = float(km_driven)
    var3 = float(mileage)
    var4 = float(engine)
    var5 = float(horsepower)
    var6 = float(seats)
    var7 = (fuel_type)
    var8 = (transmission_type)
    var9 = structural_damage
    

    fuel_list={'petrol':0,'diesel':0,'electric':0,'lpg':0,'cng':0}
    if var7 in fuel_list:
        fuel_list[var7]=1
        
    transmission_list={'manual':0,'automatic':0}
    if var8 in transmission_list:
        transmission_list[var8]=1

    damage_list={'none':0,'low':0,'moderate':0}
    if var9 in damage_list:
        damage_list[var9]=1

    pred = model.predict(np.array([var1,var2,var3,var4,var5,var6,fuel_list['diesel'],fuel_list['electric'],fuel_list['lpg'],fuel_list['petrol'],transmission_list['manual'],damage_list['moderate'],damage_list['none']]).reshape(1, -1))
    pred = round(pred[0])

    price = str(pred)

    

    # cng requirement
    if(fuel_type == "petrol"):
        cng_req = "50K - 60K"
    else:
        cng_req = "Not Applicapable"

    abs_sys = "8K - 9K"
    nav_sys = "10K - 15K"

    # cheap car
    if(pred <=300000):
        seat_cover = pred*0.04
        # structural_damage
        if(structural_damage == "low"):
            damage_profit = pred*0.01
        elif(structural_damage == "moderate"):
            damage_profit = pred*0.005
        else:
            damage_profit = "Nil"
        

    # moderate car
    elif(pred > 300000 and pred < 700000):
        seat_cover = pred*0.03
        # structural_damage
        if(structural_damage == "low"):
            damage_profit = pred*0.01
        elif(structural_damage == "moderate"):
            damage_profit = pred*0.005
        else:
            damage_profit = "Nil"
        
    # expensive car
    else:
        seat_cover = pred*0.005
        # structural_damage
        if(structural_damage == "low"):
            damage_profit = pred*0.005
        elif(structural_damage == "moderate"):
            damage_profit = pred*0.001
        else:
            damage_profit = "Nil"
        

    if(damage_profit=="Nil"):
        context['damage_profit'] = "Nil"
    else:
        context['damage_profit']= round(damage_profit,2)
    context['seat_cover'] = round(seat_cover,2)
    context['cng_req'] = cng_req
    context['abs_sys'] = abs_sys
    context['nav_sys'] = nav_sys
    context['price']=price

    print(model.score(x_test,y_test))
        
    ins = CarDetails(car_age=car_age, km_driven=km_driven, mileage=mileage, horsepower=horsepower, price=pred)
    ins.save()

    return render(request, 'result.html', context)

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    return render(request, 'contactus.html')