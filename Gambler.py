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
            origLeng = len(current.index)
            dfLeng = len(oddsDF.index)

            #print(current.head())
            #fullDF = pandas.concat([current,oddsDF],axis=0).drop_duplicates(['home_team','name','bookmakers.title']).sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)

            #deal with the fact that there are fewer items in the new set than already in the sheet.
            for x in range(len(current.index)):
                for y in range(len(oddsDF.index)):

                    if (current.loc[x,'home_team']==oddsDF.loc[y,'home_team'] and current.loc[x,'bookmakers.title']==oddsDF.loc[y,'bookmakers.title'] and current.loc[x,'name']==oddsDF.loc[y,'name']):
                        if x==y:
                            break
                        else:
                            print("adding chunk of missing values to current from new list")
                            print(oddsDF.loc[x:y-1,:])
                            current = current.append(oddsDF.loc[x:y-1,:]).sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)
                            break
                    #oddsDF = oddsDF.sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)
                    if y == len(oddsDF.index)-1:
                        print("match for current value not found, adding to new list")
                        oddsDF = oddsDF.append(current.loc[x,['name','price','point','home_team','away_team','bookmakers.title','commence_time']])
                        oddsDF = oddsDF.sort_values(["home_team",'bookmakers.title','name'],ignore_index=True)
                if x == len(current.index)-1 and len(current.index)< len(oddsDF):
                    print("adding end of new frame")
                    current = current.append(oddsDF.loc[x+1:,['name','price','point','home_team','away_team','bookmakers.title','commence_time']])
                    print(current.tail)
                    break

            #current = current.sort_index().reset_index(drop=True)
            
                
                
            #switch these after testing
            oddsDF = oddsDF.rename(columns={'price':f'price{runNum}','point':f'point{runNum}'}).drop(['home_team','away_team','bookmakers.title','commence_time','name'],axis=1)
            #oddsDF = oddsDF.rename(columns={'price':f'price{runNum}','point':f'point{runNum}'}).drop(['away_team','bookmakers.title','name'],axis=1)
            newDF = pandas.concat([current,oddsDF],axis=1)
            
            newDF.to_csv(fileName)
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])