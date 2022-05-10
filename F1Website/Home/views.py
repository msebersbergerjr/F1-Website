from distutils.command.clean import clean
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from Home import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Race_History_Serializers
import datetime
import time

# <-------------------- Misc -------------------->
def is_ajax(request):
    """
    is_ajax got deprecated, so I made my own
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_team_name(team_id):
    """
    @params: team id
    @returns: team name
    """
    return (models.Constructor.objects.filter(team_id=team_id).values('team_name')[0]['team_name'])

# <-------------------- Landing Page -------------------->
def landing(request):
    """
    Landing Page
    """
    return render(request, "Home/landing.html")

# <-------------------- Drivers Page -------------------->
def drivers_page(request, pk):
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

    return render(request, "Home/drivers_page.html", context)
    

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

    # Circuit_ID for value; Circuit_Name for Display
    circuit_dirty = models.Race_History.objects.filter(driver_id=pk).order_by('circuit_id').values('circuit_id').distinct()
    circuits = []
    for _ in circuit_dirty:
        circuits.append(models.Circuit.objects.filter(circuit_id=_['circuit_id']).values('circuit_id','circuit_name'))

    # Team_ID for value; Team_Name for Display
    team_dirty = models.Race_History.objects.filter(driver_id=pk).order_by('team_id').values('team_id').distinct()
    teams = []
    for _ in team_dirty:
        teams.append(models.Constructor.objects.filter(team_id=_['team_id']).values('team_id','team_name'))

    # Test for Chart.js
    x = models.Race_History.objects.filter(driver_id=pk).order_by('season').values('circuit_id','true_time')
    chart_data = []

    for _ in x:
        item = {
            'circuit_id': _['circuit_id'],
            'true_time': _['true_time'],
        }
        chart_data.append(item)

    context = {
        'driver_data':driver_data,
        'season': models.Race_History.objects.filter(driver_id=pk).order_by('-season').values('season').distinct(),
        'circuits': circuits,
        'teams':teams,
        'statuses': models.Race_History.objects.filter(driver_id=pk).values('status').distinct(),
        'chart_data': chart_data
    }
        

    return render(request, "Home/driver_page.html", context)

@api_view(['GET'])
def get_race_history(request,pk):
    print(request)
    season = request.query_params.get('season',None)
    circuit_id = request.query_params.get('circuit_id',None)
    team_id = request.query_params.get('team_id',None)
    status = request.query_params.get('status',None)
    race = models.Race_History.objects.filter(driver_id=pk).values('season','round','circuit_id','date','team_id','position','points','status')
    data = []
    if season:
        race = race.filter(season=season).order_by('-round')
    if circuit_id:
        race = race.filter(circuit_id=circuit_id).order_by('-season')
    if team_id:
        race = race.filter(team_id=team_id)
    if status:
        race = race.filter(status=status)
    if race:
        for _ in race:
            circuit_id = models.Circuit.objects.filter(circuit_id=_['circuit_id']).values('circuit_name')
            team_id = models.Constructor.objects.filter(team_id=_['team_id']).values('team_name')
            item = {
                'season':_['season'],
                'round': _['round'],
                'circuit_id': circuit_id[0]['circuit_name'] ,
                'date':_['date'],
                'team_id':team_id[0]['team_name'],
                'position':_['position'],
                'points':_['points'],
                'status':_['status'],
            }
            data.append(item)
        serialized = Race_History_Serializers(data, many=True)
        return Response(serialized.data)
    else:
        return Response({})

@api_view(['GET'])
def get_driver_chart(request,pk):
    circuit_id = request.query_params.get('circuit_id',None)
    labels = []
    data = []
    status = []
    chart_data = models.Race_History.objects.filter(driver_id=pk, circuit_id=circuit_id).order_by('season').values('season','true_time','status')

    for _ in chart_data:
        print(_['true_time'])
        try:
            dirty_time = datetime.datetime.strptime(_['true_time'], "%H:%M:%S.%f")
        except:
            dirty_time = datetime.datetime.strptime(_['true_time'], "%H:%M:%S")
        clean_time = dirty_time - datetime.datetime(1900,1,1)
        seconds = clean_time.total_seconds()


        labels.append(_['season'])
        data.append(seconds)

        # if _['true_time'] == '0:00:00':
        #     status.append(_['status'])
        # else:
        #     status.append(_['true_time'])
        status.append(_['true_time'])
    
    return JsonResponse({'labels':labels,'data':data,'status':status})

@api_view(['GET'])
def get_season_team_points_chart(request):
    season = request.query_params.get('season',None)

    dirty_data = models.Constructor_Standing.objects.filter(season=season).values('team_id','points')

    labels = []
    data = []
    for _ in dirty_data:

        labels.append(get_team_name(_['team_id']))
        data.append(_['points'])
    
    return JsonResponse({'labels':labels,'data':data})

# <-------------------- Teams Page -------------------->
def teams_page(request):

    context = {
        'seasons': models.Constructor_Standing.objects.order_by('-season').values('season').distinct()
    }

    return render(request, "Home/teams_page.html", context)

@api_view(['GET'])
def teams_page_ajax(request):
    season = request.query_params.get('season',None)

    data_dirty = models.Constructor_Standing.objects.filter(season=season).order_by('-points').values('team_id', 'points')
    data_clean = []

    for _ in data_dirty:
        team_name = models.Constructor.objects.filter(team_id=_['team_id']).values('team_name')
        drivers_dirty = models.Driver_Standing.objects.filter(season=season,team_id=_['team_id']).values('driver_id').distinct()

        # Get ever driver who drove for the team in season
        drivers_clean = []
        for i in drivers_dirty:
            drivers_name = models.Driver.objects.filter(driver_id=i['driver_id']).values('givenName','familyName')

            driver = {
                'givenName': drivers_name[0]['givenName'],
                'familyName': drivers_name[0]['familyName']
            }
            drivers_clean.append(driver)

        teams = {
            'team_id': _['team_id'],
            'team_name': team_name[0]['team_name'],
            'points': _['points'],
            'drivers': drivers_clean
        }
        data_clean.append(teams)

    return JsonResponse({'year':season,'teams':data_clean})
    

def team_page(request,pk):

    data_dirty = models.Constructor.objects.filter(team_id=pk).values('team_id','team_name','nationality')
    points = models.Constructor_Standing.objects.filter(team_id=pk).aggregate(Sum('points'))
    wins = models.Constructor_Standing.objects.filter(team_id=pk).aggregate(Sum('wins'))
    drivers_dirty = models.Driver_Standing.objects.order_by('-season').filter(team_id=pk).values('driver_id')[:2]
    drivers = []


    for _ in drivers_dirty:
        drivers_name = models.Driver.objects.filter(driver_id=_['driver_id']).values('givenName','familyName','driver_id')
        driver = {
            'driver_id': drivers_name[0]['driver_id'],
            'givenName': drivers_name[0]['givenName'],
            'familyName': drivers_name[0]['familyName']
        }
        drivers.append(driver)

    for _ in data_dirty:
        team_data ={
            'team_id': _['team_id'],
            'team_name': _['team_name'],
            'points': points['points__sum'],
            'wins': wins['wins__sum'],
            'nationality': _['nationality'],
            'drivers': drivers,
        }
    
    context = {
        'team_data': team_data
    }

    return render(request, "Home/team_page.html", context)

# <-------------------- Results Page -------------------->
def results_page(request, pk):

    return render(request, "Home/results_page.html")