from json import load
from pymongo import MongoClient
from __init__ import getLogger
from dotenv import load_dotenv
from datetime import datetime
import os
import json
import pandas as pd

load_dotenv()
logging = getLogger(__name__)
class DataRep():

    def __init__(self) -> None:
        _mongohost = os.getenv("mongohost")
        _mongoport = os.getenv("mongoport")
        try:
            self.conn = MongoClient(_mongohost,int(_mongoport))
            self.db = self.conn['Utilities']
            logging.info("Successfully established the connection")
        except Exception as e:
            logging.error(f"Error establishing connection {e}")

    def postholidays(self,holidaylist):
        try:
            self.col = self.db['Holidays']
            self.col.insert_many(json.loads(holidaylist))
            logging.debug("Loaded Successfully...")
            status = json.dumps({"status":200, "statusdesc":"File Loaded Successfully...."})
        except Exception as e:
            logging.error(f"Exception during loading the data --> {e}")
            status = json.dumps({"status":-100, "statusdesc":"Error loading the data" + e})
        return status

    def getholidays(self,year):
        self.col = self.db['Holidays']
        logging.debug(f"Getting data for the year {year}")
        outcursor = self.col.find({"Year":int(year)},{"_id":0})
        outobj = pd.DataFrame(list(outcursor))
        outobj['DateType'] = pd.to_datetime(outobj['Date'],format='%Y%m%d')
        outobj['Date'] =  outobj['DateType'].dt.strftime('%d-%m-%Y')
        return outobj

    def getloadexists(self,date,asset):
        self.pricedb = self.conn['Price']
        fildate = datetime.strptime(date,'%Y%m%d')
        fidate = datetime.strftime(fildate,'%d-%b-%Y').upper()
        self.output = {}
        for asst in asset:
            print(asst)
            self.col = self.pricedb[asst]
            _loadexists = 'N'
            print(fidate)
            print(self.col.count_documents({"TIMESTAMP":fidate},limit=1));
            if (self.col.count_documents({"TIMESTAMP":fidate},limit=1) == 0):
                _loadexists = 'N'
            else:
                _loadexists = 'Y'
            self.output[asst]= _loadexists
        return json.dumps(self.output)
