import asyncio
import websockets
import requests
import os 
import json
from datetime import date, timedelta 
import schwabdev
import webbrowser 

historical_data_url = "https://api.tradier.com/v1/markets/history"
session_auth_url    = "https://api.tradier.com/v1/markets/events/session"


Stock_List = ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"]

""" client = schwabdev.Client("snaHLsmvGivMq6vDDPwBzM4U0YQY6GEf", "Pv3FIPlYzTq39ccN")
client.update_tokens_auto()
streamer = client.stream
streamer.start()
streamer.send(streamer.level_one_quote("AMD","0,1,2,3,4,5"))
 """


def connect_to_schwab(app_key,secret):
    callback_url = "127.0.0.1"
    auth_url = f'https://api.schwabapi.com/v1/oauth/authorize?client_id={app_key}&redirect_uri={callback_url}'
    webbrowser.open(auth_url)
    red_link = input("Redirect Link")
    code = f"{red_link[red_link.index('code=') + 5:red_link.index('%40')]}@"
    print(code)
async def scan(ticker):
    # Look for Potential Prior Bar Low Break on Big Caps
    # Get Previous Day OCHL data 
    yt_date = date.today()-timedelta(days=1)
    try: 
        pd = requests.get(historical_data_url,
                      params={'symbol': ticker['symbol'], 'interval': 'daily', 'start': yt_date, 'end': date.today(), 'session_filter': 'open'},
                      headers={'Authorization': 'Bearer '+api_key, 'Accept': 'application/json'} )
        pd_json = pd.json()
        current_stock_price = float(ticker['price'])
        yt_low              = float(pd_json["history"]['day'][0]['low'])
        #Check if the stock price is less than 200 and currently $1 away from the PDL, then Alert
        if ( current_stock_price <= 200 and (current_stock_price - yt_low) <= 1):
            print (f"Send Alert (1 + ) - {ticker['symbol']}")
        elif (current_stock_price > 200 and  current_stock_price < 400 and (current_stock_price - yt_low) <= 1.5 ):
            print (f"Send Alert (200 + ) - {ticker['symbol']}")
        #SMCI AVGO ETC 
        elif(current_stock_price > 400 and (current_stock_price - yt_low) <= 5):
            print (f"Send Alert (400+) - {ticker['symbol']}")	      
    except Exception as error :
        #print (f"Error Occured while fetching daily data for  {ticker['symbol']}")
        print ("Error Occured while fetching daily data for", error)

    

#Connect to the web socket Server 
async def ws_connect(sl):
    uri = "wss://ws.tradier.com/v1/markets/events"
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = '{"symbols": ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ SESSION_ID +'", "filter": ["trade"], "linebreak": true}'
        await websocket.send(payload)
        async for ticker in websocket:
            #print(f"<<< {ticker}")
            # Multiple Threads 
            await scan(json.loads(ticker))
connect_to_schwab("snaHLsmvGivMq6vDDPwBzM4U0YQY6GEf","Pv3FIPlYzTq39ccN")
#asyncio.run(ws_connect(Stock_List))