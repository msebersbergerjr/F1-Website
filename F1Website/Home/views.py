import json, operator, requests
import os
import pandas as pd
from django.http.request import HttpHeaders
from django.http import response
from django.shortcuts import render

# Return driver information for all current 2021 drivers
# for home.html
def home(request):
#<-------------------- API -------------------->

    #API request to get current 2021 F1 driver standings data
    #http://ergast.com/mrd/
    # response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')
    
    #Returns JSON object
    # geodata = response.json()

    # driver_data = geodata['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']


#<-------------------- Local Storage -------------------->

    #<---------- Writing ---------->
    # Write when pulling from the API
    # with open(r'../data/current_standings.json', 'w') as outfile:
    #     json.dump(driver_data, outfile)

    #<---------- Reading ---------->
    # path = os.path.join("data", "current_standings.json")
    with open("../data/current_standings.json") as json_file:
        driver_data = json.load(json_file)

    context = {
        'driver_data': driver_data
    }

    return render(request, 'Home/home.html', context)

# Return the driver information and race results of the driver for driver_page.html
# Requires pk = driverId
def driver_page(request, pk):
#<-------------------- API -------------------->
    # #API request to get all information of current standing drivers
    # #http://ergast.com/mrd/
    # response = requests.get(f'http://ergast.com/api/f1/current/driverStandings.json')
    # geodata = response.json()

    # driver_data = geodata['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    #API request to get all race results of the selected driver (pk)
    #http://ergast.com/mrd/
    # response = requests.get(f'http://ergast.com/api/f1/drivers/{pk}/results.json?limit=500')
    # geodata = response.json()

    # result_data = geodata['MRData']['RaceTable']['Races']
    # Sort race results from Latest to Oldest by Season then Round
    # result_data.sort(key = lambda i: (get_season(i), get_round(i)), reverse=True)

#<-------------------- Local Storage -------------------->

    #<---------- Writing ---------->
    # Write when pulling from the API
    # with open(f'../data/results/{pk}_results.json', 'w') as outfile:
    #     json.dump(result_data, outfile)

    #<---------- Reading ---------->
    # cs_path = os.path.join("data", "current_standings.json")
    with open("../data/current_standings.json") as json_file:
        driver_data = json.load(json_file)

    # r_path = os.path.join("data/results", f"{pk}_results.json")
    with open(f"../data/results/{pk}_results.json") as json_file:
        result_data = json.load(json_file)





    # load into Pandas
    # df = pd.json_normalize(result_data)

    # df['Time'] = ""

    # def extractTime(x) -> str:
    #     """
    #     Extracts the course time from Results
    #     """
    #     raw = x[0]
    #     raw_dict = raw['Time']
    #     print(raw_dict['time'])
    #     return str(raw_dict['time'])

    # df["Time"] = df["Results"].apply(lambda x: extractTime(x))
    # df.head(20)

    # subset = df[['season','Circuit.circuitName', 'Results']]

    # print(subset)


    # Search driverID until it matches with PK which is the driverID
    # of the selected driver
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

# Orders by lexicographical order so we need to cast as int
def get_season(result_data): return int(result_data.get('season'))
def get_round(result_data): return int(result_data.get('round'))

# Performance history of the track for the driver
# y-axis - Speed
# x-axis - Year
def performence_histroy(request, pk):

    year = []
    time = []

    r_path = os.path.join("data/results", f"{pk}_results.json")
    with open(r_path) as json_file:
        result_data = json.load(json_file)