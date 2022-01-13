import pandas
from datetime import date

THRESHHOLD = 3

def CheckBets(sport, num):
    if num>1:
        today = str(date.today())
        fileName = sport+today+".csv"
        oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
        overs = oddsDF.loc[oddsDF['name'].str.contains("Over", case=False)]
        #oddsDF['point'] - oddsDF[f'point{num}'] > THRESHHOLD and oddsDF['name'] == "Over"
        unders = oddsDF.loc[oddsDF['name'].str.contains("Under", case=False)]
        print(overs)
        print(unders)
        overs = overs[overs['point'] - overs[f'point{num}'] > THRESHHOLD]
        unders = unders[unders['point']-unders[f'point{num}'] <- THRESHHOLD]
        print(overs)
        print(unders)
        
        
        oddsDF = pandas.concat([overs,unders])
        fileName = sport + 'BETS.csv'
        oddsDF.to_csv(fileName)
#CheckBets('basketball_nba', 2)
