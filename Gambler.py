import requests
import pandas
import json
import ToPandas
import os.path
from datetime import date
import numpy as np




# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = '195ea6f9cccf6e2c4e568757d10f0b83'

#SPORT = 'basketball_nba' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'totals' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

def checkSports():
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports', 
        params={
            'api_key': API_KEY
        }
    )


    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

    else:
        print('List of in season sports:', sports_response.json())

def getOdds(sport, runNum):
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        print('Number of events:', len(odds_json))
        oddsDF = ToPandas.pds(odds_json).sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)
       
        today = str(date.today())
        fileName = sport+today+".csv"
        if not(os.path.exists(fileName)):
            oddsDF.to_csv(fileName)
        else:
            
            current = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
            difference = len(current.index)-len(oddsDF.index)
            if difference>0:
                #deal with the fact that there are fewer items in the new set than already in the sheet.
                print(difference)
                missingTeams = set(oddsDF.iloc[:,3]).symmetric_difference(set(current.iloc[:, 3]))
                empty = pandas.DataFrame(np.full((difference,7), np.nan),columns=oddsDF.columns)
                oddsDFFixed = pandas.concat((empty,oddsDF))
                
                print(missingTeams)
                print(len(missingTeams))
                numFilled = 0
                for ind, team in enumerate(missingTeams):
                    
                    numToFill = current['home_team'].value_counts.team
                    oddsDF.iloc[numFilled:numToFill,3]=team
                    numFilled += numToFill
                oddsDF = oddsDF.sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)


            oddsDF = oddsDF.rename(columns={'price':f'price{runNum}','point':f'point{runNum}'}).drop(['home_team','away_team','bookmakers.title','commence_time','name'],axis=1)
            
            newDF = pandas.concat([current,oddsDF],axis=1)
            newDF.to_csv(fileName)
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])