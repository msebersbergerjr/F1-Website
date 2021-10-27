import requests, json, os.path, io
from tqdm import tqdm

#<-------------------- Misc -------------------->
'''
Check if file exist & if not create one
'''
def fileCheck(path):
    if ~(os.path.isfile(path) and os.access(path, os.R_OK)):
        with io.open(os.path.join(path), 'w') as outfile:
            outfile.write(json.dumps({}))

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
path = os.path.join("data")
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
        path = os.path.join("data","results")
        to_file = os.path.join(path, f'{driver}_results.json')

        fileCheck(to_file)

        with open(to_file, 'w') as outfile:
            json.dump(result_data, outfile)

        pbar.update()
    pbar.close()





