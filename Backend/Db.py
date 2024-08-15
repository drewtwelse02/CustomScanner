import sqlite3
import DisplayColor as printinfo
class DB:
    def __init__(self):
        printinfo.info("Loading Database")
        #Check if the database already exist, If not create it 
        self.conn = sqlite3.connect("cs.db")
        # Intialize the strategy tables 
        self.initialize_pdl_tb ()

    def initialize_pdl_tb (self):
        # Check to see if the table exists already 
        res = self.conn.execute("SELECT name FROM sqlite_master")
        if (res.fetchone() is None):
            printinfo.info("Table for PDL does not exists, creating it ...")
            # Create the new Table 
            res_pdl = self.conn.execute ("CREATE TABLE PDL (ticker_id, ticker_symbol, pdl_price)")
            print(res_pdl.description)

