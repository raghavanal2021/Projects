from json import load
from nis import match
from pymongo import MongoClient
from __init__ import getLogger
from dotenv import load_dotenv
from datetime import datetime,timedelta
import os
import json
import pandas as pd
import requests
load_dotenv()
logging = getLogger(__name__)
class DataRep:

    _utilurl = os.getenv("util_url")
    def __init__(self) -> None:
        _mongohost = os.getenv("mongo_host")
        _mongoport = os.getenv("mongo_port")
        
        try:
            self.conn = MongoClient(_mongohost,int(_mongoport))
            self.db = self.conn['Price']
            logging.info("Successfully established the connection")
        except Exception as e:
            logging.error(f"Error establishing connection {e}")

    def get_business_days(self,todate,lookbackperiod):
        end_date = datetime.strptime(todate,'%Y%m%d')
        start_date = end_date- timedelta(days=30)
        start_date_str = start_date.strftime('%Y%m%d')
        end_date_str = end_date.strftime('%Y%m%d')
        url = f"{self._utilurl}/businessdays/{start_date_str}/{end_date_str}"
        r = requests.get(url)
        resp = json.loads(r.text)
        bus_df = pd.read_json(resp)
        bus_df = bus_df.set_index(bus_df['BDate']).sort_index()
        out = bus_df['BDate'].tail(lookbackperiod)
        date_list = [datetime.strptime(str(date), "%Y%m%d") for date in list(out)]
        return date_list
    
    def get_equity_candle_data(self,todate,lookbackperiod):
        date_list = self.get_business_days(todate,lookbackperiod)
        self.equity_coll = self.db['Equity']
        logging.info(f"Getting data for {date_list}")
        outcandles = self.equity_coll.find({"dates":{"$in":date_list}},{"_id":0})
        df = pd.DataFrame(list(outcandles))
        return df
    
    def set_narrowrange(self,data,type):
        self.db = self.conn['Screeners']
        self.coll = self.db[type]
        print(data)
        self.coll.insert_many(data)
        return 100

    def get_narrowrange(self,date):
        dat = datetime.strptime(date,'%Y%m%d')
        self.db = self.conn['Screeners']
        self.coll = self.db['NarrowRange4']
        out = self.coll.find({"dates":dat},{"_id":0})
        df = pd.DataFrame((list(out)))
        print(df)
        return df.to_json(orient='records',date_format='iso')