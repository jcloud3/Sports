from unicodedata import name
import pandas
from datetime import date
import smtplib, ssl
import os.path
#need to hide email password in system variable later
THRESHHOLD = 3.5
def SendEmail(bets):
    port = 465  # For SSL
    password = "Makememoney123"

    # Create a secure SSL context
    context = ssl.create_default_context()
    sender_email = "cloudj820@gmail.com"
    receiver_email = "6305614363@mms.att.net"
    message = ''
    for index,row in bets.iterrows():
        message += row[5] + " " + row[0] + ' ' + row[3] + ' ' + str(row[8])+'\n'
    if len(message)<160:
        message += ' '*(161 - len(message))

# Send email here
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("cloudj820@gmail.com", password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)

def CheckBets(sport):
    today = str(date.today())
    fileName = sport+today+".csv"
    if (os.path.exists(fileName)):
        oddsDF = pandas.read_csv(fileName).drop(columns='Unnamed: 0')
        #previousBets = pandas.read_csv(sport + 'BETS.csv').drop(columns='Unnamed: 0')
        num = int(((len(oddsDF.columns)-5)/2))
        if num>1:
            overs = oddsDF.loc[oddsDF['name'].str.contains("Over", case=False)]
            #oddsDF['point'] - oddsDF[f'point{num}'] > THRESHHOLD and oddsDF['name'] == "Over"
            unders = oddsDF.loc[oddsDF['name'].str.contains("Under", case=False)]
            
            overs = overs[overs['point'] - overs[f'point{num}'] > THRESHHOLD]
            unders = unders[unders['point']-unders[f'point{num}'] <- THRESHHOLD]
            
            
            
            oddsDF = pandas.concat([overs,unders],ignore_index=True)
            print(oddsDF)
        # if len(oddsDF) > 0:
            # SendEmail(oddsDF)
            fileName = sport + 'BETS.csv'
            oddsDF.to_csv(fileName)
#CheckBets('basketball_ncaab')

def CheckViability():
    #loop through each line and check any pair of odds for a given match
    #implied probability must be < 100% for a bet to be viable
    
    return 0

def ImpliedProbability(odds1,odds2):
    return 1/odds1 + 1/odds2


def StakeCalculation(odds1,odds2,stake1):
    #this results in the largest possible win if you think team 1 will win
    team1towin = stake1/(odds2-1)

    #this results in the largest possible win if you think team 2 will win
    team2towin = stake1*(odds1-1) 

    return team1towin, team2towin





