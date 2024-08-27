import sqlite3
import DisplayColor as printinfo
import Session
import statistics
from datetime import date
class DB:
    def __init__(self):
        #printinfo.info("Checking Database Status")
        #Check if the database already exist, If not create it 
        self.conn = sqlite3.connect("cs.db")
        self.s = Session.Session()
        # Intialize the strategy tables 
        #self.initialize_pdl_tb ()

    def initialize_pd_tb (self):
        # Check to see if the table exists already 
        res = self.conn.execute("SELECT * FROM sqlite_master")
        if (res.fetchone() is None):
            printinfo.info("Tables do not exist, creating them ...")
            # Create the new Table for prior day data (OHLC)
            res_pd = self.conn.executescript ("""
                                              CREATE TABLE PD (ticker_symbol,date, pdo_price, pdl_price, pdh_price,pdc_price);
                                              CREATE TABLE STDDEV (ticker_symbol,date,std_dev);
                                              """)
            # Return True if the table was created 
            return True
        else:
            printinfo.info("PD Table Already created...")
            return False 
    async def load_last_pd_data(self,stock_list):
        printinfo.info("Loading Prior day Data ")
        for ticker in stock_list:
            d_info = await self.s.get_yt_daily_data(ticker)
            #print(d_info['history']['day']['open'])
            data = [ticker,d_info['history']['day']['date'],d_info['history']['day']['open'],d_info['history']['day']['low'],d_info['history']['day']['high'],d_info['history']['day']['close']]
            self.conn.execute("INSERT INTO PD(ticker_symbol,date,pdo_price,pdl_price,pdh_price,pdc_price) VALUES (?,?,?,?,?,?)",data)
            self.conn.commit()

        r = self.conn.execute("SELECT * FROM PD")
        if (r.fetchone() is not None):
            printinfo.info("Prior Days Data Loaded Successfully")
        
    def load_std_Dev (self,stock_list):
        printinfo.info("Loading Std Dev ... ")
        for ticker in stock_list : 
            vol_aggs = self.s.get_last_volume_bars(ticker)
            std_dev = statistics.stdev(vol_aggs)
            #print( ticker + " STD Dev is " + str(std_dev))
            data = [ticker,date.today(),std_dev]
            self.conn.execute("INSERT INTO STDDEV (ticker_symbol,date,std_dev) VALUES (?,?,?)",data)
            self.conn.commit()
        
        r = self.conn.execute("SELECT * FROM STDDEV")
        if (r.fetchone() is not None):
            #print(r.fetchall())
            printinfo.info("Prior Days Data Loaded Successfully")
    async def get_daily_data_from_db(self,symbol):
        r = self.conn.execute("SELECT * FROM PD WHERE ticker_symbol=?",(symbol,))
        return r.fetchall()




 