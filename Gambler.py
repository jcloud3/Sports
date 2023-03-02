import requests
import pandas
import json
import ToPandas
import os.path
from datetime import date, datetime, timedelta
import numpy as np
#need to hide api key in system variable later





'''dont think this is needed anymore as there will not be a need to open existing csv. Should be able to make decisions in each pandas df '''
def openExisting(fileName, oddsDF):
    current = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
    runNum = int(((len(current.columns)-5)/2)+1)
    difference = len(current.index)-len(oddsDF.index)
    origLeng = len(current.index)
    dfLeng = len(oddsDF.index)
    #switch these after testing
    oddsDF = oddsDF.rename(columns={'price':f'price{runNum}','point':f'point{runNum}'}).drop(['home_team','away_team','bookmakers.title','commence_time','name'],axis=1)
    #oddsDF = oddsDF.rename(columns={'price':f'price{runNum}','point':f'point{runNum}'}).drop(['away_team','bookmakers.title','name'],axis=1)
    print(len(oddsDF.index))
    print(len(current.index))
    
    newDF = pandas.concat([current,oddsDF],axis=1)
    
    newDF.to_csv(fileName)

# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = 'ef569f22e002a9b39a8df3f173ee03eb'

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

def getOdds(sport):
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
        if len(odds_json) > 0:
            print('Number of events:', len(odds_json))

            oddsDF = ToPandas.pds(odds_json).sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)
            oddsDF=oddsDF.sort_values(["commence_time"],ignore_index=True)
            tomorrowday = (datetime.today()+ timedelta(days = 1)).strftime('%Y-%m-%d')
            tomDateTime = tomorrowday +'T09:00:00Z'
            indOfTomorrow = len(np.where(oddsDF.loc[:,'commence_time']<tomDateTime)[0])
            if indOfTomorrow < len(oddsDF.index):
                tomorrow = oddsDF.iloc[indOfTomorrow:,:].sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)
                tomorrowFile = sport+tomorrowday+'.csv'
                if not(os.path.exists(tomorrowFile)):
                # print(indOfTomorrow)
                    tomorrow.to_csv(tomorrowFile)
                else:
                    openExisting(tomorrowFile,tomorrow)
                oddsDF = oddsDF.iloc[:indOfTomorrow,:]
            oddsDF = oddsDF.sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)
            today = str(date.today())
            fileName = sport+today+".csv"
            if not(os.path.exists(fileName)):
                oddsDF.to_csv(fileName)
                
            else:
                openExisting(fileName,oddsDF)
                    
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])


