import json, operator, requests, os, io
import pandas as pd
from django.http.request import HttpHeaders
from django.http import response
from django.shortcuts import render
import datetime as dt
from datetime import datetime, timedelta

#<-------------------- Misc -------------------->
'''
Check if file exist & if not create one
'''
def fileCheck(path):
    if not os.path.isfile(path) and os.access(path, os.R_OK):
        with io.open(os.path.join(path), 'w') as outfile:
            outfile.write(json.dumps({}))

'''
Orders by lexicographical order, so we get value 
& cast as int
'''
def get_season(result_data): return int(result_data.get('season'))
def get_round(result_data): return int(result_data.get('round'))

def home(request):
    '''
    @return: driver information for current standings
    '''
#<-------------------- Local Storage -------------------->
    #<---------- Reading ---------->
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, 'current_standings.json')

    fileCheck(to_file)

    with open(to_file) as json_file:
        driver_data = json.load(json_file)

    context = {
        'driver_data': driver_data
    }

    return render(request, 'Home/home.html', context)

def constructor_home(request):
    '''
    @return: constructor information for current constructors & drivers for team
    '''

    #<---------- Reading ---------->
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, 'current_constructor.json')

    fileCheck(to_file)

    with open(to_file) as json_file:
        constructor_data = json.load(json_file)

    context = {
        'constructor_data': constructor_data
    }

    return render(request, 'Home/constructor_home.html', context)

def constructor_page(request, pk):
    '''
    @return: current team information for each team
    @parms pk = constructorId
    '''
#<-------------------- Local Storage -------------------->
    #<---------- Reading ---------->
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, 'current_constructor.json')

    fileCheck(to_file)

    with open(to_file) as json_file:
        constructor_data = json.load(json_file)

    count = 0
    for i in constructor_data:
        if i['constructorId'] == pk:
            break
        count += 1

    context = {
        'constructor_data': constructor_data[count]
    }

    return render(request, 'Home/constructor_page.html', context)

def driver_page(request, pk):
    '''
    @return: current standings and race results for each driver
    @parms pk = driverId
    '''
#<-------------------- Local Storage -------------------->
    #<---------- Reading ---------->
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, 'current_standings.json')

    fileCheck(to_file)

    with open(to_file) as json_file:
        driver_data = json.load(json_file)

    path = os.path.join("F1Website", "data", "results")
    to_file = os.path.join(path, f'{pk}_results.json')

    fileCheck(to_file)

    with open(to_file) as json_file:
        result_data = json.load(json_file)

    '''
    Search driverID until it matches with PK which is the driverID
    of the selected driver
    '''
    count = 0
    for i in driver_data:

        if i['Driver']['driverId'] == pk:
            break
        count += 1

    context = {
        'driver_data': driver_data[count],
        'result_data': result_data
    }

    return render(request, 'Home/driver_page.html', context)