import pandas
from datetime import date

THRESHHOLD = 3.5

def CheckBets(sport):
    today = str(date.today())
    fileName = sport+today+".csv"
    oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
    num = int(((len(oddsDF.columns)-5)/2))
    if num>1:
        overs = oddsDF.loc[oddsDF['name'].str.contains("Over", case=False)]
        #oddsDF['point'] - oddsDF[f'point{num}'] > THRESHHOLD and oddsDF['name'] == "Over"
        unders = oddsDF.loc[oddsDF['name'].str.contains("Under", case=False)]
        
        overs = overs[overs['point'] - overs[f'point{num}'] > THRESHHOLD]
        unders = unders[unders['point']-unders[f'point{num}'] <- THRESHHOLD]
        
        
        
        oddsDF = pandas.concat([overs,unders])
        fileName = sport + 'BETS.csv'
        oddsDF.to_csv(fileName)
#CheckBets('basketball_ncaab', 6)
