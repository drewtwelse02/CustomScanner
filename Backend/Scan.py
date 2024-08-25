from Db import DB
import json
import DisplayColor as printinfo
async def pdl_scan(ticker):
    # Look for Potential Prior Bar Low Break on Big Caps
    # Get Previous Day OCHL data from DB 
    db = DB()
    j = json.loads(ticker)
    current_price = await db.get_daily_data_from_db(j['symbol'])
    if (current_price == j['price']):
        printinfo.info(f"{j['symbol']} is currently at Prior day low ")        
