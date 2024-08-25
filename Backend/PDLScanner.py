import asyncio
import websockets
from datetime import date, timedelta
from StdDev import StdDev
from Session import Session
import json
from Db import DB
import Scan

Stock_List = ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BAC","AXP","MS","JPM","FDX","UPS","AMZN"]

# Initialize Market Session from Tradier 
tradier_session = Session()
session_id =tradier_session.get_session_id()

# Launch Database Engine 
db = DB()
# Check if PD table needs to be loaded 
if (db.initialize_pd_tb() is True ):
    asyncio.run(db.load_last_pd_data(Stock_List))
    db.load_std_Dev(Stock_List)


#Connect to the web socket Server 
async def ws_connect(sl):
    uri = "wss://ws.tradier.com/v1/markets/events"
    std_dev = StdDev()
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = '{"symbols": ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BAC","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ session_id +'", "filter": ["trade"], "linebreak": true}'
        await websocket.send(payload)
        async for ticker in websocket:
            # Multiple Threads 
            await Scan.pdl_scan(ticker)

asyncio.run(ws_connect(Stock_List))
