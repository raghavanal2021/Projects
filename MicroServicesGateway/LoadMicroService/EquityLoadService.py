'''
Equity Load Service
'''
from LoadtoMongo import MongoLoad
from __init__ import getLogger
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
import json
from datetime import datetime
import requests, os
from dotenv import load_dotenv
import pandas as pd
from DownloadandUnzip import DownloadandUnzip
import redis
#Set the Logger
load_dotenv()
logging = getLogger(__name__)
utilities_url = os.getenv("UTILITIES_URL")
equities_url = os.getenv("EQUITIES_URL")
logging.info(f"{utilities_url} found !! ")
class EquityLoad():
    '''
    Loads Equity files from NSE Website
    '''

    name = "service_equityload"
    download = DownloadandUnzip()
    _redishost = os.getenv("redishost")
    _redisport = os.getenv("redisport")
    red =  redis.StrictRedis(host=_redishost,port=_redisport,charset='utf-8', decode_responses=True)
    mongoload = MongoLoad()

    @event_handler("service_loader","equityload")
    def handle_event(self, payload):
        logging.info(f"Received Payload : {payload}")
        print(payload)
        try:
            msgObj = eval(payload)  
            startDate = msgObj['startDate']
            endDate = msgObj['endDate']
            assetClass = msgObj['assetClass']
            loadoptions = msgObj['options']
            self.prepareload(startDate,endDate,loadoptions)
        except Exception as e:
            logging.error(e)

    def prepareload(self,startDate,endDate,loadoptions):
        try:
            startdate_obj = datetime.strptime(startDate,'%Y%m%d')
            enddate_obj = datetime.strptime(endDate,'%Y%m%d')
            self.filename = []
            logging.info(f"Starting load between {startdate_obj} and {enddate_obj}")
            #Get Business Dates between the dates
            datelist = self.get_business_days(startDate,endDate)
            for dates in datelist:
                fil = self.get_equity_file_name(dates)
                fildate = datetime.strptime(dates,'%Y%m%d')
                r = requests.get(f"{utilities_url}/loadexists/{datetime.strftime(fildate,'%Y%m%d')}")
                loadcheckresponse = json.loads(r.json())
                if loadcheckresponse['Equity'] == 'N':
                    year_date = fildate.year
                    year_month = datetime.strftime(fildate,'%b').upper()
                    downloadurl = f"{equities_url}/{year_date}/{year_month}/{fil}"
                    print(downloadurl)
                    status = self.download.downloadfile(downloadurl,fil,'equity')
                    if status == 100 :
                        message = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"asset":'Equity','reporttype':'price',"statuscode":200, "statusdesc":f"Equity file {fil} is successful.","date":dates}}
                        self.red.publish("loadstatus",json.dumps(message))
                else:
                    message = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"asset":'Equity','reporttype':'price',"statuscode":-100, "statusdesc":f"Data Already Exists. Not downloading again. ","date":dates}}
                    self.red.publish("loadstatus",json.dumps(message))
            self.mongoload.equity_load('equity')
        except Exception as e:
            logging.error(f"Error converting to Date format {e}")   


    def get_business_days(self,startDate,endDate):
            bday_url = f"{utilities_url}/businessdays/{startDate}/{endDate}"
            r = requests.get(bday_url) 
            bday_response = json.loads(r.json())
            return list(bday_response['BDate'].values())
    
    def get_equity_file_name(self,datestr):
        dateobj = datetime.strptime(datestr,'%Y%m%d')
        fileout = f"cm{dateobj.strftime('%d%b%Y').upper()}bhav.csv.zip"
        print (fileout)
        return fileout

#https://archives.nseindia.com/content/historical/EQUITIES/2022/APR/cm06APR2022bhav.csv.zip