import pandas
from datetime import datetime, timedelta

THRESHHOLD = 2



def CheckBets(sport, num, thresh,book=''):
    results = pandas.DataFrame([[sport,thresh,num,0,0,0,0.0]],columns=['sport','THRESHHOLD','runNum','win','loss','push','price'])
    if num>1:
        yesterday = (datetime.today()- timedelta(days = 1)).strftime('%Y-%m-%d')
        fileName = sport+yesterday+".csv"
        oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
        overs = oddsDF.loc[oddsDF['name'].str.contains("Over", case=False)]
        #oddsDF['point'] - oddsDF[f'point{num}'] > THRESHHOLD and oddsDF['name'] == "Over"
        unders = oddsDF.loc[oddsDF['name'].str.contains("Under", case=False)]
        
        overs = overs[overs['point'] - overs[f'point{num}'] > THRESHHOLD]
        unders = unders[unders['point']-unders[f'point{num}'] <- THRESHHOLD]
        
        if book!='':
            overs = overs[overs['bookmakers.title'].str.contains(book,case=False)]
            unders = unders[unders['bookmakers.title'].str.contains(book,case=False)]
        
        overs['result'] = overs[f'point{num}']<overs['total_score']
        results['win'] = overs.result.sum()
        results['loss'] = (overs[f'point{num}']>overs['total_score']).sum()
        results['push'] = (overs[f'point{num}']==overs['total_score']).sum()
        unders['result'] = unders[f'point{num}']>unders['total_score']
        results['win'] += unders.result.sum()
        results['loss'] += (unders[f'point{num}']<unders['total_score']).sum()
        results['push'] = (unders[f'point{num}']==unders['total_score']).sum()
        
        print(overs)
        print(unders)
        oddsDF = pandas.concat([overs,unders])
        #need to fix this. Should only get price of winning bets
        if(results.loc[0,'win']>0):
            results['price'] = oddsDF[oddsDF['result']][f'price{num}'].mean()*results['win']-(results['win']+results['loss'])
        #print(oddsDF)
        else:
            results['price'] = -(results['win']+results['loss'])
        
        return results
        fileName = sport + 'BETS.csv'
        #oddsDF.to_csv(fileName)
def Loopthrough():
    df = pandas.DataFrame()
    for run in range(3):
        for thresh in range(THRESHHOLD):
            #df = pandas.concat([df,CheckBets('basketball_ncaab',run,thresh,book='betrivers')])
            df = pandas.concat([df,CheckBets('basketball_nba',run,thresh)])
            df.to_csv("nbaresults.csv")
    

#CheckBets('basketball_nba',5)
Loopthrough()