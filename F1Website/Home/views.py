import json
from django.http import response
from django.shortcuts import render
import requests

# Create your views here.
def home(request):

    # response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')
    # geodata = response.json()

    # print(json.dumps(geodata, indent=2))

    # driver_data = geodata['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    # with open('current.json', 'w') as outfile:
    #     json.dump(driver_data, outfile)

    with open(r"C:\Users\oknis\OneDrive\Documents\Websites\F1\F1-Website\standings.json") as json_file:
        driver_data = json.load(json_file)

    # print(json.dumps(driver_data, indent=2))

    # for i in driver_data:

    #     print(i['Constructors'][0]['constructorId'])
    
    # for i in driver_data:
    #     print(i['Driver']['driverId'])

    context = {
        'driver_data': driver_data
    }

    return render(request, 'Home/home.html', context)

def driver_page(request, pk):

    # print(pk)

    # response = requests.get(f'http://ergast.com/api/f1/drivers/{pk}/results.json?limit=500')
    # geodata = response.json()

    # print(json.dumps(geodata, indent=2))

    # driver_data = geodata['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    # result_data = geodata['MRData']['RaceTable']['Races']

    # print(json.dumps(result_data, indent=2))

    # with open('results.json', 'w') as outfile:
    #     json.dump(result_data, outfile)

    with open(r"C:\Users\oknis\OneDrive\Documents\Websites\F1\F1-Website\standings.json") as json_file:
        driver_data = json.load(json_file)

    with open(r"C:\Users\oknis\OneDrive\Documents\Websites\F1\F1-Website\results.json") as json_file:
        result_data = json.load(json_file)

    count = 0

    for i in driver_data:

        if i['Driver']['driverId'] == pk:
            break
        count += 1

    # print(json.dumps(driver_data[count], indent=2))

    context = {
        'driver_data': driver_data[count],
        'result_data': result_data
    }

    return render(request, 'Home/driver_page.html', context)