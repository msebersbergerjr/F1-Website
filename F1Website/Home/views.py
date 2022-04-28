import json, os, io
import pandas as pd
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from Home import models

# <-------------------- Misc -------------------->
def is_ajax(request):
    """
    is_ajax got deprecated, so I made my own
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# <-------------------- Lineup Page -------------------->
def lineup_page(request, pk):
    """
    @parm: select year
    @returns: 
    information the lineup page needs for the cards
    Current selected year
    years to choose from for dropdown
    """

    # Get ordered list by MOST points of drivers within the selected year
    # Clean it and organize it in a way for the html to easily read
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
    
# <-------------------- Landing Page -------------------->
def landing(request):
    """
    Landing Page
    """
    return render(request, "Home/landing.html")

# <-------------------- Driver Page -------------------->
def driver_page(request, pk):
    """
    @parm: driver_id
    @returns:
    Driver related information from models
    Points from models
    Wins from models
    """

    data_dirty = models.Driver.objects.filter(driver_id=pk).values('permanentNumber','givenName','familyName','nationality','dateOfBirth')
    points = models.Driver_Standing.objects.filter(driver_id=pk).aggregate(Sum('points'))
    wins = models.Driver_Standing.objects.filter(driver_id=pk).aggregate(Sum('wins'))

    for _ in data_dirty:
        driver_data = {
        'givenName': _['givenName'],
        'familyName': _['familyName'],
        'permanentNumber': _['permanentNumber'],
        'points': points['points__sum'],
        'wins': wins['wins__sum'],
        'nationality': _['nationality'],
        'dateOfBirth':_['dateOfBirth']
        }

    context = {
        'driver_data':driver_data
    }

    return render(request, "Home/driver_page.html", context)
