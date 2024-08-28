from Db import DB
import json
import DisplayColor as printinfo
async def pdl_scan(ticker):
    # Look for Potential Prior Bar Low Break on Big Caps
    # Get Previous Day OCHL data from DB 
    printinfo.info("Looking for potential PBL break")
    db = DB()
    j = json.loads(ticker)
    res   = await db.get_daily_data_from_db(j['symbol'])
    prev_day_low = float(res[0][3])
    current_price  = float(j['price'])
    # Detect Prior Bar Low cross Over 
    # For stocks below 250, it should start Alerting 30 cents prior to the potential Cross 
    if (current_price < 250.00 ):
        if (prev_day_low == current_price  or (abs(current_price - prev_day_low)< 0.30)):
            printinfo.info(f"{j['symbol']} is currently at or close to the  Prior day low ")
    # For stocks below 500, it should start Alerting 30 cents prior to the potential Cross  
    elif (current_price >= 250.00 and current_price < 500.00 ): 
        if (prev_day_low == current_price  or (abs(current_price - prev_day_low)< 0.60)):
            printinfo.info(f"{j['symbol']} is currently at or close to the  Prior day low ")   
