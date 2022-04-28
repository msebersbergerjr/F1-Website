import json, os, io
from django.http import JsonResponse
from django.views import View
import pandas as pd
from django.shortcuts import render
from urllib3 import HTTPResponse
from Home import models

# <-------------------- Misc -------------------->
"""
Check if file exist & if not create one
"""
def fileCheck(path):
    if not os.path.isfile(path) and os.access(path, os.R_OK):
        with io.open(os.path.join(path), "w") as outfile:
            outfile.write(json.dumps({}))\

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def lineup_page(request, pk):
    
    data_dirty = models.Driver_Standing.objects.filter(season=pk).order_by('-points').values('driver_id','team_id','points','wins')

    data_clean = []

    for _ in data_dirty:
        extra = models.Driver.objects.filter(driver_id=_['driver_id']).values('permanentNumber','givenName','familyName','nationality')

        driver = {
            'driver_id': _['driver_id'],
            'givenName': extra[0]['givenName'],
            'familyName': extra[0]['familyName'],
            'permanentNumber': extra[0]['permanentNumber'],
            'team_id': _['team_id'],
            'points': _['points'],
            'wins': _['wins'],
            'nationality': extra[0]['nationality'],
        }
        data_clean.append(driver)
    
    context = {
        'year': pk,
        'drivers': data_clean,
        'seasons': models.Driver_Standing.objects.order_by('-season').values('season').distinct()
    }

    return render(request, "Home/lineup_page.html", context)
    

def home(request):

    return render(request, "Home/home.html")


def constructor_home(request):
    """
    @return: constructor information for current constructors & drivers for team
    """

    # <---------- Reading ---------->
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, "current_constructor.json")

    fileCheck(to_file)

    with open(to_file) as json_file:
        constructor_data = json.load(json_file)

    context = {"constructor_data": constructor_data}

    return render(request, "Home/constructor_home.html", context)


def constructor_page(request, pk):
    """
    @return: current team information for each team
    @parms pk = constructorId
    """
    # <-------------------- Local Storage -------------------->
    # <---------- Reading ---------->
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, "current_constructor.json")

    fileCheck(to_file)

    with open(to_file) as json_file:
        constructor_data = json.load(json_file)

    count = 0
    for i in constructor_data:
        if i["constructorId"] == pk:
            break
        count += 1

    context = {"constructor_data": constructor_data[count]}

    return render(request, "Home/constructor_page.html", context)


def driver_page(request, pk):
    """
    @return: current standings and race results for each driver
    @parms pk = driverId
    # """
    # <-------------------- Local Storage -------------------->
    # <---------- Reading ---------->
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, "current_standings.json")

    fileCheck(to_file)

    with open(to_file) as json_file:
        driver_data = json.load(json_file)

    """
    Search driverID until it matches with PK which is the driverID
    of the selected driver
    """
    count = 0
    for i in driver_data:

        if i["Driver"]["driverId"] == pk:
            break
        count += 1

    context = {"driver_data": driver_data[count]}

    return render(request, "Home/driver_page.html", context)

def get_race_history(request):

    seasons = ['2022','2021','2000']

    return render(request, "Home/race_history.html", {'seasons':seasons})
