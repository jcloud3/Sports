from datetime import datetime, timedelta
from sportsipy.nba.boxscore import Boxscores
import pandas

def getFinalScores():
    sport = 'basketball_nba'
    yesterday = datetime.today()- timedelta(days = 1)
    games_today = Boxscores(yesterday)
    date = yesterday.strftime('%-m-%d-%Y')
    print (games_today.games.keys())
    df = pandas.DataFrame.from_dict(games_today.games[date]).drop(['boxscore','losing_abbr','losing_name','winning_abbr','winning_name','home_abbr','away_abbr'],axis=1)
    df['total_score'] = df['away_score'] + df['home_score']
    #print(df)
    if sport == 'basketball_nba':
        df['home_name'] = df['home_name'].where(df['home_name']!='LA Clippers','Clippers')
        df['home_name'] = df['home_name'].where(df['home_name']!='LA Lakers','Lakers')
    #print(df)
    fileName = sport+yesterday.strftime('%Y-%m-%d')+'.csv'
    oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
    #oddsDF['total_score'] = oddsDF['home_team']
    #print(oddsDF.loc[oddsDF['home_team'].str.contains('Brooklyn', case=False)])
    for index, row in df.iterrows():
    
        oddsDF.loc[oddsDF['home_team'].str.contains(row.loc['home_name'],case=False),['total_score']] = row.loc['total_score']

    oddsDF.to_csv(fileName)
#getFinalScores()
