# F1 Driver Stats Website ![badge](https://img.shields.io/badge/license-Open-brightgreen) [![GitHub version](https://badge.fury.io/gh/Naereen%2FStrapDown.js.svg)](https://github.com/msebersbergerjr/F1-Website)

# Table of Contents
    
* [About](#about)
* [Local Installation](#local-installation)
* [Preview](#preview)
* [Future Goals](#future-goals)
* [Contributing](#contributing)


# About 
    
This is a project to pull data from a Formula One driver statistics API to inform users on race updates, built using [Django](https://www.djangoproject.com/).

The data is pulled from [Ergast Developer API](http://ergast.com/mrd/), which provides a historical record of motor racing data for non-commercial purposes
    

# Dependencie Libraries
    
* [django](https://www.djangoproject.com)
* [requests](https://docs.python-requests.org/en/latest/)
* [pandas](https://pandas.pydata.org/)
* [tqdm](https://pypi.org/project/tqdm/)    
    
# Local Installation

## Setup
Before running this program, make sure to install all the required libraries from requirement.txt

```
> pip install -r requriment.txt
    or
> pip3 install -r requriment.txt
```

## Running
Once all libraries are installed, to run:
* Makefile:
```
> make preach
```
* Manually:
cd into the F1Website directory
```
> cd F1Website/
> python manage.py runserver
    or
> python3 manage.py runserver
```

# Updating the Database
update.py - to update the local database with the most up-to-date information provided by [Ergast Developer API](http://ergast.com/mrd/)

It then formats and stores the data using both JSON & CSV for the website to access and read from

| WARNING |
|:---------------------------|
| This can take anywhere from 5-7 mins |

To update the database with the latest race information:
* F1-Website directory
```
> python update.py
    or
> python3 update.py
```




# Preview 

### The production build is coming soon!
#### Desktop View
[![github-f1preview.png](https://i.postimg.cc/ncrykd6B/github-f1preview.png)](https://postimg.cc/9r3gXBXQ)

# Future Goals

* Data Visualization
* Makefile re-write
* Automatically run update.py every Sunday evening to ensure the website is always up-to-date
* Constructor page providing historical and current information about the said constructor
* Count down the clock to when the next race takes an event
* Track page to provide historical information about the said track
* Implement a system to automatically remove the endless supply of py cache that gets generated

# Contributing
    
Pull requests are welcome, but we encourage issues to be opened should you find bugs or would like to make feature requests.

Contributors
- [@msebersbergerjr](https://github.com/msebersbergerjr)
- [@okni-c AKA Kevin Dallas Yatsinko](https://github.com/okni-c)
