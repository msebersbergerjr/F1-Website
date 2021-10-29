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


def convertH(raw_time):
    '''
    Convert to datetime.timedelta object in format: H:M:S.Mic
    '''

    dirty_time = datetime.strptime(raw_time,'%I:%M:%S.%f').time()
    clean_time = timedelta(hours=dirty_time.hour, minutes=dirty_time.minute, seconds=dirty_time.second, microseconds=dirty_time.microsecond)

    return clean_time

def convertM(raw_time):
    '''
    Convert to datetime.timedelta object in format: M:S.Mic
    '''

    dirty_time = datetime.strptime(raw_time,'%M:%S.%f').time()
    clean_time = timedelta(minutes=dirty_time.minute, seconds=dirty_time.second, microseconds=dirty_time.microsecond)

    return clean_time

def convertS(raw_time):
    '''
    Convert to datetime.timedelta object in format: S.Mic
    '''

    dirty_time = datetime.strptime(raw_time,'%S.%f').time()
    clean_time = timedelta(seconds=dirty_time.second, microseconds=dirty_time.microsecond)

    return clean_time

def convertMill(raw_time):
    '''
    Rare case data goes over 60 in minutes and doesnt convert properly
    '''

    mill = dt.timedelta(milliseconds=int(raw_time.split('.',1)[1]))
    sec = dt.timedelta(seconds=int(raw_time[:2]))
    clean_time = sec + mill

    return clean_time


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

#TODO
def performence_histroy(request, pk):

    year = []
    time = []

    '''
    Read laptime into dataframe
    '''
    path = os.path.join("F1Website", "data")
    to_file = os.path.join(path, 'laptime.csv')
    dot = 'csv'

    fileCheck(to_file, dot)

    laptime_df = pd.read_csv(to_file)

    '''Get selected drivers race history'''
    path = os.path.join("F1Website","data", "results")
    # to_file = os.path.join(path, f'{pk}_results.json')

    #<---------- Testing ---------->
    to_file = os.path.join(path, 'mazepin_results.json')

    dot = 'json'

    fileCheck(to_file,dot)

    with open(to_file) as json_file:
        result_data = json.load(json_file)

    count = 0

    for race in result_data:
        
        i = laptime_df.index[(laptime_df['season'] == int(race['season'])) & (laptime_df['round'] == int(race['round'])) & (laptime_df['circuitId'] == race['Circuit']['circuitId'])].tolist()
        # print(race['season'], race['round'], race['Circuit']['circuitId'])
        '''
        if: driver one that race, take time
        else: get driver time and add to time of 1st place
        '''
        if(laptime_df.loc[i]['driverId'] == race['Results'][0]['Driver']['driverId']).all():
            '''convert driver time to type time'''
            try:
                track_time = convertH(race['Results'][0]['Time']['time'])
                print(track_time, race['season'] ,race['round'], race['Circuit']['circuitId'], race['Results'][0]['Driver']['driverId'])
                #print(f"From JSON {race['Results'][0]['Time']['time']}  |  Datetime {dirty_time}  |  Timedelta {track_time}  |  {race['season']} {race['round']} {race['Circuit']['circuitId']} {race['Results'][0]['Driver']['driverId']}")
                
            except:
                track_time = convertM(race['Results'][0]['Time']['time'])
                print(track_time, race['season'] ,race['round'], race['Circuit']['circuitId'], race['Results'][0]['Driver']['driverId'])
                #print(f"From JSON {race['Results'][0]['Time']['time']}  |  Datetime {dirty_time}  |  Timedelta {track_time}  |  {race['season']} {race['round']} {race['Circuit']['circuitId']} {race['Results'][0]['Driver']['driverId']}")

            year.append([race['season']])
            time.append(track_time)

        else:
            '''Check if they Finished Race'''
            if race['Results'][0]['status'] == 'Finished':

                '''Strip the '+' infront of the time'''
                raw_time = race['Results'][0]['Time']['time']
                dirty_time = raw_time[1:]

                '''for the RARE case there is a 's' in the time'''
                if dirty_time[-1] == 's':
                    dirty_time = dirty_time[:-1]

                '''for the Rare case the seconds go over 60 and DONT convert'''
                try:
                    int(dirty_time[:2])
                
                except ValueError:

                    try:
                        clean_time = convertM(dirty_time)
                    except:
                        clean_time = convertS(dirty_time)

                else:
                    clean_time = convertMill(dirty_time)
                
                '''Get 1st place time and make it a timedelta object'''
                x = laptime_df.loc[i]['time'].item()
                try:
                    first_time = convertH(x)
                except:
                    first_time = convertM(x)

                '''Add time to 1st place time to get track_time'''
                track_time = clean_time + first_time
                year.append([race['season']])
                time.append(track_time)
                print( track_time, race['season'] ,race['round'], race['Circuit']['circuitId'], race['Results'][0]['Driver']['driverId'])
                #print(f'Tracktime: {first_time}  +  Drivertime {clean_time}  =  Totaltime {track_time}')
                #print(f"From CSV {x}  |  Datetime {y}  |  Timedelta {first_time}  |  {race['season']} {race['round']} {race['Circuit']['circuitId']} {race['Results'][0]['Driver']['driverId']}")

            else:
                '''Time dictionary does NOT exist if NOT Finished'''
                #print(race['Results'][0]['status'])
                track_time = timedelta(seconds=0, microseconds=0)
                year.append([race['season']])
                time.append(track_time)

    return response.JsonResponse(date={
        'year': year,
        'time': time
    })