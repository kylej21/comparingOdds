import json
import requests
import pandas as pd
import time
pd.set_option('display.max_rows', None)
sportsRecieve = []

# An api key is emailed to you when you sign up to a plan
API_KEY = '707f98bcf9f78833e11059728a4f9be8'

TYPE = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports', 
    params={
        'api_key': API_KEY
    }
)


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

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
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])

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
    print("what game would you like to see the odds for? Print the number corresponding")
    gameNum=(int(input))
    print()
    idx=0
    hosts=[]
    winWeight=[]
    drawWeight=[]
    lossWeight=[]
    for x in bookmakers[gameNum]:
        
        hosts.append(x["key"])
        
        winWeight.append(x["outcomes"][0]["price"])
        drawWeight.append(x["outcomes"][2]["price"])
        lossWeight.append(x["outcomes"][1]["price"])
    
    
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])