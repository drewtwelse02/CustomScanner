import asyncio
import websockets
from datetime import date, timedelta
from StdDev import StdDev
from Session import Session
import Scan
import json
import Tools
from Db import DB

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
    cummulated_vol = {"AAPL":0,"GOOGL":0,"RDDT":0,"MSTR":0,"MARA":0,"COIN":0,"MU":0,"QCOM":0,"AMD":0,"AVGO":0,"NVDL":0,"SMCI":0,"TSLA":0,"RIVN":0,"WFC":0,"GS":0,"BAC":0,"AXP":0,"MS":0,"JPM":0,"FDX":0,"UPS":0,"AMZN":0}
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = '{"symbols": ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BAC","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ session_id +'", "filter": [""], "linebreak": true}'
        await websocket.send(payload)
        async for ticker in websocket:
            j_ticker = json.loads(ticker)
            # Multiple Threads
            if(j_ticker["type"] == "trade"):
                await Scan.pdl_scan(ticker)
            elif(j_ticker["type"] == "timesale"):
                print(Tools.convert_date(float(j_ticker["date"])))


asyncio.run(ws_connect(Stock_List))
