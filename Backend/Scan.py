from Db import DB
import json
import DisplayColor as printinfo
async def pdl_scan(ticker):
    # Look for Potential Prior Bar Low Break on Big Caps
    # Get Previous Day OCHL data from DB 
    printinfo.info("Looking for potential PBL break")
    db = DB()
    j = json.loads(ticker)
    current_price = await db.get_daily_data_from_db(j['symbol'])
    #print (f"PDL is {}")
    print(j['price'])
    if (float(j['price']) == float(current_price[0][3])):
        printinfo.info(f"{j['symbol']} is currently at Prior day low ")        
