import asyncio
import websockets
import requests
import os 
import json
from datetime import date, timedelta 

historical_data_url = "https://api.tradier.com/v1/markets/history"
session_auth_url    = "https://api.tradier.com/v1/markets/events/session"

# Create Market Session 
api_key = os.environ['TRADIER_API_KEY']
response = requests.post(session_auth_url,
    data={},
    headers={'Authorization': 'Bearer '+str(api_key), 'Accept': 'application/json'})

response_json = response.json()
SESSION_ID = response_json.get("stream")['sessionid']

def scan(ticker):
    # Look for Potential Prior Bar Low Break on Big Caps
    # Get Previous Day OCHL data 
    yt_date = date.today()-timedelta(days=1)
    try: 
        pd = requests.get(historical_data_url,
                      params={'symbol': ticker['symbol'], 'interval': 'daily', 'start': yt_date, 'end': date.today(), 'session_filter': 'open'},
                      headers={'Authorization': 'Bearer '+api_key, 'Accept': 'application/json'} )
        pd_json = pd.json()
        current_stock_price = float(ticker['price'])
        yt_low              = float(pd_json["history"]["day"]['low'])
        #print(current_stock_price)
        #Check if the stock price is less than 200 and currently $1 away from the PDL, then Alert
        if ( current_stock_price <= 200 and (current_stock_price - yt_low) <= 1):
            print(f"Send Alert - {ticker['symbol']}")
        elif (current_stock_price > 200 and  current_stock_price < 400 and (current_stock_price - yt_low) <= 1.5 ):
            print ("200-400 Alert ")
        elif(current_stock_price > 400 and (current_stock_price - yt_low) <= 30):
            print (f" 400 + {ticker['symbol']}")
    except :
        print (f"Error Occured while fetching daily data for  {ticker['symbol']}")

    

    

#Connect to the web socket Server 
async def ws_connect():
    uri = "wss://ws.tradier.com/v1/markets/events"
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = '{"symbols": ["AAPL","AMZN","TSLA","GOOGL","RDDT","RIVN","FDX", "SMCI"], "sessionid": "'+ SESSION_ID +'", "filter": ["trade"], "linebreak": true}'
        await websocket.send(payload)

        #print(f">>> {payload}")
        async for ticker in websocket:
            #print(f"<<< {ticker}")
            # Multiple Threads 
            scan(json.loads(ticker))

asyncio.run(ws_connect())