import json
import requests
import pandas as pd
import time
pd.set_option('display.max_rows', None)
sportsRecieve = []
#
#
#
#
#
#HERE IS WHERE TO INPUT THE API KEY FROM YOUR EMAIL INSIDE OF THE ''!!!!
API_KEY = ''

TYPE = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix


sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports', 
    params={
        'api_key': API_KEY
    }
)


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{TYPE}/odds',
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
    # Check the usage quota
    for x in odds_json:
        sportsRecieve.append(x["sport_key"])

sports = pd.Series(sportsRecieve)
print(sports)
print("Please input the number corresponding to the sport you want to know the odds of: ")
time.sleep(3)
sport = sports_response.json()[int(input())]
#print(sport)

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{sport["key"]}/odds',
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
    #print(odds_json)
    games = []
    bookmakers=[]
    winName=""
    lossName=""
    for x in odds_json:
        bookmakers.append(x["bookmakers"])
        games.append([x["home_team"],x["away_team"],])
    out = []
    for x in games:
        out.append(x[0] + " vs " + x[1])
    gamesFin = pd.Series(out)
    print(gamesFin)
    print("what game would you like to see the odds for? Print the number corresponding")
    gameNum=(int(input()))
    print()
    idx=0
    hosts=[]
    winWeight=[]
    #drawWeight=[]
    lossWeight=[]
    for x in bookmakers[gameNum]:
        hosts.append(x["key"])
        winWeight.append(float(x["markets"][0]["outcomes"][0]["price"]))
        #try:
            #drawWeight.append(float(x["markets"][0]["outcomes"][2]["price"]))
        #except:
           # pass
        lossWeight.append(float(x["markets"][0]["outcomes"][1]["price"]))
    #if drawWeight is not []:
        #rates = pd.DataFrame({'host' : hosts, 'win weight' : winWeight, 'draw weight' : drawWeight, 'loss weight' : lossWeight})
    #else:
    rates = pd.DataFrame({'host' : hosts, 'win weight' : winWeight, 'loss weight' : lossWeight})
    avgWin = sum(winWeight)/len(hosts)
    #avgDraw = sum(drawWeight)/len(hosts)
    avgLoss = sum(lossWeight)/len(hosts)
    print("what is the win weight on your app: e.x 1.3")
    inpWin = input()
    print("what is the loss weight on your app: e.x 2.3")
    inpLoss = input()
    #print("what is the draw weight on your app (if no draws input 0): e.x 2.4")
    #inpDraw = input()
    print(rates)
    outputted = False
    if float(inpWin) > avgWin:
        print("The payout for a win is likely to payout more than it statistically should. ")
        outputted=True
    if float(inpLoss) > avgLoss:
        print("The payout for a loss is likely to payout more than it statistically should")
        outputted=True
    if outputted == False:
        print("your app has no favorable bets for this event")
    #if inpDraw > drawWeight and drawWeight != 0:
     #   print("The payout for a draw is likely to payour more than it statistically should") 

    print("average win weight: " + str(avgWin))
    #if sum(drawWeight) != 0:
    #    print("average draw weight: " + str(avgDraw))
    #else:
      #  print("no draws")
    print("average loss weight: " + str(avgLoss))

    
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])