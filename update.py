from numpy import empty
import requests, json, os.path, io, pandas as pd
import datetime as dt
from datetime import datetime, timedelta
from tqdm import tqdm

#<-------------------- Misc -------------------->
'''
Check if file exist & if not create one
also checks the . extension for the file
'''
def fileCheck(path, dot):
    if dot == 'json':
        if not os.path.isfile(path) and os.access(path, os.R_OK):
            with io.open(os.path.join(path), 'w') as outfile:
                outfile.write(json.dumps({}))
    if dot == 'csv':
        if not os.path.isfile(path) and os.access(path, os.R_OK):
            with io.open(os.path.join(path), 'w') as outfile:
                pass

# '''
# Orders by lexicographical order so we need to cast as int
# '''
# def get_season(result_data): return int(result_data.get('season'))
# def get_round(result_data): return int(result_data.get('round'))

# #<-------------------- Current Standings -------------------->
# '''
# API request to get all information of current standing drivers
# http://ergast.com/mrd/
# '''
# response = requests.get(f'http://ergast.com/api/f1/current/driverStandings.json')

# #Returns JSON object
# geodata = response.json()

# #Dictionary hopping
# current_standings_data = geodata['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

# #<---------- Writing ---------->
# '''
# Write sorted result_data
# Compatible path for any OS
# '''
# path = os.path.join("F1Website", "data")
# to_file = os.path.join(path, 'current_standings.json')

# fileCheck(to_file)

# with open(to_file, 'w') as outfile:
#     json.dump(current_standings_data, outfile)

# #<-------------------- Driver Page -------------------->
# '''
# Request Race Results for each driver by getting all current drivers for the season
# and requesting each ones data from 'http://ergast.com/mrd/'
# '''
# current_drivers = []

# for driver in current_standings_data:
#     current_drivers.append(driver['Driver']['driverId'])

# with tqdm(total=len(current_drivers), ascii=False) as pbar:
#     '''
#     Command line progress bar
#     '''
#     for driver in current_drivers:
#         '''
#         API request to get all race results of the selected driver (pk)
#         http://ergast.com/mrd/
#         '''
#         response = requests.get(f'http://ergast.com/api/f1/drivers/{driver}/results.json?limit=500')
        
#         #Returns JSON object
#         geodata = response.json()
        
#         #Dictionary hopping
#         result_data = geodata['MRData']['RaceTable']['Races']

#         '''
#         Sort race results from Latest to Oldest by Season then Round
#         '''
#         result_data.sort(key = lambda i: (get_season(i), get_round(i)), reverse=True)

#         #<---------- Writing ---------->
#         '''
#         Write sorted result_data
#         Compatible path for any OS
#         '''
#         path = os.path.join("F1Website", "data", "results")
#         to_file = os.path.join(path, f'{driver}_results.json')

#         fileCheck(to_file)

#         with open(to_file, 'w') as outfile:
#             json.dump(result_data, outfile)

#         pbar.update()
#     pbar.close()


# #<-------------------- Performence History -------------------->

# '''
# Gets the 1st place last time for every race in a given year to be used as a base for
# the performence history of drivers who didn't finish in 1st place
# '''

# years = ['2021','2020','2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001']

# df = pd.DataFrame(columns=['season','round','circuitId','time','driverId'])

# with tqdm(total=len(years), ascii=False) as pbar:
#     '''
#     Command line progress bar
#     '''
#     for year in years:
#         '''
#         API request to get all race results of the given year
#         http://ergast.com/mrd/
#         '''
#         response = requests.get(f'http://ergast.com/api/f1/{year}/results.json?limit=500')

#         # Returns JSON object
#         geodata = response.json()

#         #Dictionary hopping
#         race_results = geodata['MRData']['RaceTable']['Races']

#         '''
#         Iterate through each round in a season
#         '''
#         for race in race_results:
#             y = int(race['season'])
#             round = int(race['round'])
#             circuitId = race['Circuit']['circuitId']

#             time = race['Results'][0]['Time']['time']

#             # '''
#             # Sometimes a race is cancled or stopped due to something
#             # so this try/excepts incase there is no proper track time
#             # '''
#             # try:
#             #     time = datetime.strptime(race['Results'][0]['Time']['time'],'%I:%M:%S.%f').time()
#             # except:
#             #     time = datetime.strptime(race['Results'][0]['Time']['time'],'%M:%S.%f').time()

#             driverId = race['Results'][0]['Driver']['driverId']

#             df.loc[len(df.index)] = [y, round, circuitId, time, driverId ]

#         pbar.update()
#     pbar.close()

# '''
# Sort by Year then round Decending
# '''
# df = df.sort_values(['season', 'round'],ascending = [False, False])


# #<---------- Writing ---------->
# '''
# Write dataframe to csv
# Compatible path for any OS
# '''

# path = os.path.join("F1Website", "data")
# to_file = os.path.join(path, 'laptime.csv')
# dot = 'csv'

# fileCheck(to_file, dot)

# df.to_csv(to_file, encoding='utf-8', index=False)


'''
Read laptime into dataframe
'''
path = os.path.join("F1Website", "data")
to_file = os.path.join(path, 'laptime.csv')
dot = 'csv'

fileCheck(to_file, dot)

laptime_df = pd.read_csv(to_file)

'''
Get each driverID in current standings
'''
#<---------- Reading ---------->
path = os.path.join("F1Website","data")
to_file = os.path.join(path, 'current_standings.json')
dot = 'json'

fileCheck(to_file, dot)

with open(to_file) as json_file:
    driver_data = json.load(json_file)

current_drivers = []

for driver in driver_data:
    current_drivers.append(driver['Driver']['driverId'])

'''
Check season, circuitId, check diverId, then get the time
'''
for driver in current_drivers:

    path = os.path.join("F1Website","data", "results")
    to_file = os.path.join(path, f'{driver}_results.json')
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
                dirty_time = datetime.strptime(race['Results'][0]['Time']['time'],'%I:%M:%S.%f').time()
                track_time = timedelta(hours=dirty_time.hour, minutes=dirty_time.minute, seconds=dirty_time.second, milliseconds=dirty_time.microsecond)
                print(track_time, race['season'] ,race['round'], race['Circuit']['circuitId'], race['Results'][0]['Driver']['driverId'])
                
            except:
                dirty_time = datetime.strptime(race['Results'][0]['Time']['time'],'%M:%S.%f').time()
                track_time = timedelta(minutes=dirty_time.minute, seconds=dirty_time.second, milliseconds=dirty_time.microsecond)
                print(track_time, race['season'] ,race['round'], race['Circuit']['circuitId'], race['Results'][0]['Driver']['driverId'])
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
                        dirty_time = datetime.strptime(dirty_time,'%M:%S.%f').time()
                        clean_time = timedelta(minutes=dirty_time.minute, seconds=dirty_time.second, milliseconds=dirty_time.microsecond)
                    except:
                        dirty_time = datetime.strptime(dirty_time,'%S.%f').time()
                        clean_time = timedelta(seconds=dirty_time.second, milliseconds=dirty_time.microsecond)

                else:
                    mill = dt.timedelta(milliseconds=int(dirty_time.split('.',1)[1]))
                    sec = dt.timedelta(seconds=int(dirty_time[:2]))
                    clean_time = sec + mill

                #print(race['Results'][0]['status'], race['season'] ,race['round'],clean_time, race['Circuit']['circuitId'], race['Results'][0]['Driver']['driverId'])
                
                '''Get 1st place time and make it a timedelta object'''
                x = laptime_df.loc[i]['time'].item()
                try:
                    y = datetime.strptime(x,'%I:%M:%S.%f').time()
                    first_time = timedelta(hours=y.hour, minutes=y.minute, seconds=y.second, milliseconds=y.microsecond)
                except:
                    y = datetime.strptime(x,'%M:%S.%f').time()
                    first_time = timedelta(minutes=y.minute, seconds=y.second, milliseconds=y.microsecond)

                '''Add time to 1st place time to get track_time'''
                track_time = clean_time + first_time
                #print( track_time, race['season'] ,race['round'], race['Circuit']['circuitId'], race['Results'][0]['Driver']['driverId'])
                print(f" {first_time}  |  {x}  |  {race['season']} {race['round']} {race['Circuit']['circuitId']} {race['Results'][0]['Driver']['driverId']}")

            else:
                '''Time dictionary does NOT exist if NOT Finished'''
                #print(race['Results'][0]['status'])
                pass

        