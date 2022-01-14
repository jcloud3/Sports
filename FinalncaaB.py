from datetime import datetime, timedelta
from sportsipy.ncaab.boxscore import Boxscores
import pandas
sport = 'basketball_ncaab'
yesterday = datetime.today()- timedelta(days = 1)
games_today = Boxscores(yesterday)
date = yesterday.strftime('%-m-%d-%Y')
print (games_today.games.keys())
df = pandas.DataFrame.from_dict(games_today.games[date]).drop(['away_name','home_name','boxscore','away_rank','home_rank','non_di','top_25','losing_abbr','losing_name','winning_abbr','winning_name'],axis=1)
df['total_score'] = df['away_score'] + df['home_score']
print(df)

#df['home_abbr'] = df['home_abbr'].where(not(df['home_abbr'].str.contains('-')),df['home_abbr'].str.replace('-',' '))
#df['home_name'] = df['home_name'].where(df['home_name']!='LA Lakers','Lakers')
print(df)
fileName = sport+yesterday.strftime('%Y-%m-%d')+'.csv'
oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
#oddsDF['total_score'] = oddsDF['home_team']
#print(oddsDF.loc[oddsDF['home_team'].str.contains('Brooklyn', case=False)])
for index, row in df.iterrows():
    home = row.loc['home_abbr'].replace('-',' ')
    away = row.loc['away_abbr'].replace('-', ' ')
   
    oddsDF.loc[oddsDF['home_team'].str.contains(home,case=False),['total_score']] = row.loc['total_score']
    oddsDF.loc[oddsDF['away_team'].str.contains(away,case=False),['total_score']] = row.loc['total_score']
#print(oddsDF)
oddsDF.to_csv(fileName)