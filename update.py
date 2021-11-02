from typing import Container
from numpy import empty
import requests, json, os.path, io, pandas as pd
from tqdm import tqdm
from urllib.request import urlopen
from bs4 import BeautifulSoup

from F1Website.Home.views import constructor_home

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
print("Fetching Drivers for 2021")

with tqdm(total=1, ascii=False) as pbar:
    response = requests.get(f'http://ergast.com/api/f1/current/driverStandings.json')

    #Returns JSON object
    geodata = response.json()

    #Dictionary hopping
    current_standings_data = geodata['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    pbar.update()
    pbar.close()

#<---------- Writing ---------->
'''
Write sorted result_data
Compatible path for any OS
'''
path = os.path.join("F1Website", "data")
to_file = os.path.join(path, 'current_standings.json')
dot = 'json'

fileCheck(to_file, dot)

with open(to_file, 'w') as outfile:
    json.dump(current_standings_data, outfile)

#<-------------------- Current Constructors -------------------->
'''
API request to get all information of current standing drivers
'http://ergast.com/mrd/'
'''
print("Fetching Constructors for 2021")

with tqdm(total=1, ascii=False) as pbar:
    response = requests.get('http://ergast.com/api/f1/2021/constructors.json')

    #Returns JSON object
    geodata = response.json()

    #Dictionary hopping
    current_constructor_data = geodata['MRData']['ConstructorTable']['Constructors']
    pbar.update()
    pbar.close()

names = []
for i in current_constructor_data:
    name = i['name'].split(' ',1)
    names.append(name[0])

#-------------------- Beautiful Soup --------------------
'''
Scrap the F1 website to get extra information that the API from 'http://ergast.com/mrd/' does not provide
'''
extra = []
f1_constructor_url = 'https://www.formula1.com/en/teams.html'
print('Accessing https://www.formula1.com/en/teams.html')

request_page = urlopen(f1_constructor_url)
page_html = request_page.read()
request_page.close()
html_soup = BeautifulSoup(page_html, 'html.parser')

#-------------------- Parsing --------------------
teams = html_soup.find_all("div", class_=["col-12 col-md-6"])

'''
Get team name, points, and drivers for each team
'''
for i in teams:
    name = i.find("span", class_="f1-color--black").text
    name = name.split(' ', 1)
    
    '''Change the name to fit a easier match for the API'''
    for j in names:
        if name[0] == j:
            name = j

    points = i.find("div", class_="f1-wide--s").text
    driver_one = i.find_all("span", class_=["last-name f1-uppercase f1-bold--xs d-block d-lg-inline"])[0].text
    driver_two = i.find_all("span", class_=["last-name f1-uppercase f1-bold--xs d-block d-lg-inline"])[1].text
    team_url = i.find("a", class_=["listing-link"])
    team_url = 'https://www.formula1.com' + team_url['href']
    
    '''Get Base, Team Chief, Technical Chief, Chassis, Power Unit, 1st team entry, World Championships'''
    request_team = urlopen(team_url)
    team_html = request_team.read()
    request_team.close()
    team_soup = BeautifulSoup(team_html, 'html.parser')
    table_body = team_soup.find("table", class_=["stat-list"])
    rows = table_body.find_all('tr')

    row_info = []

    for row in rows:
        x = row.find("span", class_=["text"]).text
        y = row.find("td", class_=["stat-value"]).text
        row_info.append(y)


    '''Store this data into a tuple'''
    detail_tuple = (name, points, driver_one, driver_two, row_info)
    extra.append(detail_tuple)

'''
Match the name with the team name, then add the points and drivers to the json
'''
for i in extra:
    '''Find index of team'''
    for j, dic in enumerate(current_constructor_data):
        _name = dic['name'].split(' ',1)
        if _name[0] == i[0]:
            '''Insert new key and value pairs'''
            current_constructor_data[j]['points'] = str(i[1])
            current_constructor_data[j]['driver_one'] = str(i[2])
            current_constructor_data[j]['driver_two'] = str(i[3])
            current_constructor_data[j]['base'] = str(i[4][1])
            current_constructor_data[j]['team_chief'] = str(i[4][2])
            current_constructor_data[j]['technical_chief'] = str(i[4][3])
            current_constructor_data[j]['chassis'] = str(i[4][4])
            current_constructor_data[j]['power_unit'] = str(i[4][5])
            current_constructor_data[j]['entry'] = str(i[4][6])
            current_constructor_data[j]['world_championships'] = str(i[4][7])


#<---------- Writing ---------->
'''
Write current constructor data
Compatible path for any OS
'''
path = os.path.join("F1Website", "data")
to_file = os.path.join(path, 'current_constructor.json')
dot = 'json'

fileCheck(to_file, dot)

with open(to_file, 'w') as outfile:
    json.dump(current_constructor_data, outfile)

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


