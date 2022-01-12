import pandas
from datetime import date

THRESHHOLD = 3

def CheckBets(sport, num):
    today = str(date.today())
    fileName = sport+today+".csv"
    oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
    oddsDF['Bet'] = abs(oddsDF['point'] - oddsDF[f'point{num}']) > THRESHHOLD
    oddsDF = oddsDF[oddsDF['Bet']==True]
    fileName = sport + 'BETS.csv'
    oddsDF.to_csv(fileName)
#CheckBets('basketball_nba', 2)
CheckBets('basketball_ncaab', 2)