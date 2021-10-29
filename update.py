from numpy import empty
import requests, json, os.path, io, pandas as pd
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

'''
Orders by lexicographical order so we need to cast as int
'''
def get_season(result_data): return int(result_data.get('season'))
def get_round(result_data): return int(result_data.get('round'))

#<-------------------- Current Standings -------------------->
'''
API request to get all information of current standing drivers
http://ergast.com/mrd/
'''
response = requests.get(f'http://ergast.com/api/f1/current/driverStandings.json')

#Returns JSON object
geodata = response.json()

#Dictionary hopping
current_standings_data = geodata['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

#<---------- Writing ---------->
'''
Write sorted result_data
Compatible path for any OS
'''
path = os.path.join("F1Website", "data")
to_file = os.path.join(path, 'current_standings.json')

fileCheck(to_file)

with open(to_file, 'w') as outfile:
    json.dump(current_standings_data, outfile)

#<-------------------- Driver Page -------------------->
'''
Request Race Results for each driver by getting all current drivers for the season
and requesting each ones data from 'http://ergast.com/mrd/'
'''
current_drivers = []

for driver in current_standings_data:
    current_drivers.append(driver['Driver']['driverId'])

with tqdm(total=len(current_drivers), ascii=False) as pbar:
    '''
    Command line progress bar
    '''
    for driver in current_drivers:
        '''
        API request to get all race results of the selected driver (pk)
        http://ergast.com/mrd/
        '''
        response = requests.get(f'http://ergast.com/api/f1/drivers/{driver}/results.json?limit=500')
        
        #Returns JSON object
        geodata = response.json()
        
        #Dictionary hopping
        result_data = geodata['MRData']['RaceTable']['Races']

        '''
        Sort race results from Latest to Oldest by Season then Round
        '''
        result_data.sort(key = lambda i: (get_season(i), get_round(i)), reverse=True)

        #<---------- Writing ---------->
        '''
        Write sorted result_data
        Compatible path for any OS
        '''
        path = os.path.join("F1Website", "data", "results")
        to_file = os.path.join(path, f'{driver}_results.json')

        fileCheck(to_file)

        with open(to_file, 'w') as outfile:
            json.dump(result_data, outfile)

        pbar.update()
    pbar.close()


#<-------------------- Performence History -------------------->

'''
Gets the 1st place last time for every race in a given year to be used as a base for
the performence history of drivers who didn't finish in 1st place
'''

years = ['2021','2020','2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001']

df = pd.DataFrame(columns=['season','round','circuitId','time','driverId'])

with tqdm(total=len(years), ascii=False) as pbar:
    '''
    Command line progress bar
    '''
    for year in years:
        '''
        API request to get all race results of the given year
        http://ergast.com/mrd/
        '''
        response = requests.get(f'http://ergast.com/api/f1/{year}/results.json?limit=500')

        # Returns JSON object
        geodata = response.json()

        #Dictionary hopping
        race_results = geodata['MRData']['RaceTable']['Races']

        '''
        Iterate through each round in a season
        '''
        for race in race_results:
            y = int(race['season'])
            round = int(race['round'])
            circuitId = race['Circuit']['circuitId']

            time = race['Results'][0]['Time']['time']

            # '''
            # Sometimes a race is cancled or stopped due to something
            # so this try/excepts incase there is no proper track time
            # '''
            # try:
            #     time = datetime.strptime(race['Results'][0]['Time']['time'],'%I:%M:%S.%f').time()
            # except:
            #     time = datetime.strptime(race['Results'][0]['Time']['time'],'%M:%S.%f').time()

            driverId = race['Results'][0]['Driver']['driverId']

            df.loc[len(df.index)] = [y, round, circuitId, time, driverId ]

        pbar.update()
    pbar.close()

'''
Sort by Year then round Decending
'''
df = df.sort_values(['season', 'round'],ascending = [False, False])


#<---------- Writing ---------->
'''
Write dataframe to csv
Compatible path for any OS
'''

path = os.path.join("F1Website", "data")
to_file = os.path.join(path, 'laptime.csv')
dot = 'csv'

fileCheck(to_file, dot)

df.to_csv(to_file, encoding='utf-8', index=False)