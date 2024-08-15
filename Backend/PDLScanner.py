import asyncio
import websockets
import requests
import os 
import json
from datetime import date, timedelta
from StdDev import StdDev

historical_data_url = "https://api.tradier.com/v1/markets/history"
session_auth_url    = "https://api.tradier.com/v1/markets/events/session"
tradier_url = 'https://api.tradier.com/v1/markets/events/session'

session_id = ""

Stock_List = ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"]

try :
    response = requests.post(tradier_url,
        data={},
        headers={'Authorization': 'Bearer '+ str(os.environ.get('TRADIER_TOKEN')), 'Accept': 'application/json'}
    )
    json_response = response.json()
    #print(response.status_code)

    session_id = json_response['stream']['sessionid']
    #print(session_id)
except Exception as error:
    print("Unable to Create market Session ")
    exit()

def pdl_scan(ticker):
    # Look for Potential Prior Bar Low Break on Big Caps
    # Get Previous Day OCHL data 
    yt_date = date.today()-timedelta(days=1)
    try: 
        pd = requests.get(historical_data_url,
                      params={'symbol': ticker['symbol'], 'interval': 'daily', 'start': yt_date, 'end': yt_date, 'session_filter': 'open'},
                      headers={'Authorization': 'Bearer '+ os.environ.get('TRADIER_TOKEN'), 'Accept': 'application/json'} )
        pd_json = pd.json()
        current_stock_price = float(ticker['price'])
        yt_low              = float(pd_json["history"]['day']['low'])
        print(yt_low)
        #Check if the stock price is less than 200 and currently $1 away from the PDL, then Alert
        if ( current_stock_price <= 200 and (current_stock_price - yt_low) <= 1):
            print (f"Send Alert (1 + ) - {ticker['symbol']}")
        elif (current_stock_price > 200 and  current_stock_price < 400 and (current_stock_price - yt_low) <= 1.5 ):
            print (f"Send Alert (200 + ) - {ticker['symbol']}")
        #SMCI AVGO ETC 
        elif(current_stock_price > 400 and (current_stock_price - yt_low) <= 5 and (current_stock_price - yt_low) > 0):
            #print(ticker)
            print (f"Send Alert (400+) - {ticker['symbol']}")	      
    except Exception as error :
        #print (f"Error Occured while fetching daily data for  {ticker['symbol']}")
        print ("Error Occured while fetching daily data for", error)

#Connect to the web socket Server 
async def ws_connect(sl):
    uri = "wss://ws.tradier.com/v1/markets/events"
    std_dev = StdDev()
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = '{"symbols": ["LLY","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ session_id +'", "filter": ["trade"], "linebreak": true}'
        await websocket.send(payload)
        async for ticker in websocket:
            # Multiple Threads 
            #print(ticker)
            #pdl_scan(json.loads(ticker))
            std_dev.runstd_dev(json.loads(ticker))
asyncio.run(ws_connect(Stock_List))