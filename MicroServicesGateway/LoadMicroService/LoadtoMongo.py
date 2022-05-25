'''
Load to Mongo Database
'''
from __init__ import getLogger
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd
import redis,json
from datetime import datetime

load_dotenv()
logging = getLogger(__name__)
class MongoLoad():
    '''
    Load the records to Mongo Database
    '''
    def __init__(self):
        '''Initialize Mongo Database Connection'''
        _mongohost = os.getenv("mongo_host")
        _mongoport = int(os.getenv("mongo_port"))
        self.conn = MongoClient(_mongohost,_mongoport)
        self.db = self.conn['Price']
        self.red = redis.StrictRedis('localhost',6379,charset='utf-8', decode_responses=True)

    def equity_load(self,asset):
        '''Load Equity related files'''
        _loc = os.getenv("DATA_LOC")
        _arch = os.getenv("ARCH_LOC")
        self.location = f"{_loc}/{asset}"
        self.archlocation = f"{_arch}/{asset}"
        self.coll = self.db['Equity']
        for file in os.listdir(self.location):
            try:
                logging.info("Reading file {file}")
                fileloc = f"{self.location}/{file}"
                archloc = f"{self.archlocation}/{file}"
                df = pd.read_csv(fileloc)
                dateobj = datetime.strptime(df['TIMESTAMP'].max(),'%d-%b-%Y')
                df['dates'] = dateobj
                dateval = datetime.strftime(datetime.strptime(df['TIMESTAMP'].max(),'%d-%b-%Y'),'%Y%m%d')
                if (self.coll.count_documents({"TIMESTAMP": dateval},limit = 1) != 0):
                    logging.error(f"Attempting to load duplicate records for {dateval}")
                    interimmessage = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"date": dateval ,"asset":'Equity',"reporttype":"DB Load","statuscode":-100, "statusdesc":f"Records already exists for date {dateval}"}}
                    self.red.publish('loadstatus',json.dumps(interimmessage))
                else:
                    self.coll.insert_many(df.to_dict('records'))
                    logging.info(f"Loaded file {file}")
                    interimmessage = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"date": dateval ,"asset":'Equity',"reporttype":"DB Load","statuscode":200, "statusdesc":f"Equity File {file} loaded successfully."}}
                    self.red.publish('loadstatus',json.dumps(interimmessage))
                    self.red.publish('screenequity',dateval)
                os.rename(fileloc,archloc)
                logging.info(f"Moved {file} from {fileloc} to {archloc}")
            except Exception as e:
                logging.error(e)
                interimmessage = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"date": dateval ,"asset":'Equity',"reporttype":"DB Load","statuscode":-100, "statusdesc":f"{e}"}}
                self.red.publish('loadstatus',json.dumps(interimmessage))
        return json.dumps(interimmessage)


    def deriv_load(self,asset):
        '''Load Equity related files'''
        _loc = os.getenv("DATA_LOC")
        _arch = os.getenv("ARCH_LOC")
        self.location = f"{_loc}/{asset}"
        self.archlocation = f"{_arch}/{asset}"
        self.dbase = self.conn['Price']
        for file in os.listdir(self.location):
            try:
                self.ficoll = self.dbase['IndexFutures']
                self.fscoll = self.dbase['StockFutures']
                self.opicoll = self.dbase['IndexOptions']
                self.opscoll = self.dbase['StockOptions']
                logging.info("Reading file {file}")
                fileloc = f"{self.location}/{file}"
                archloc = f"{self.archlocation}/{file}"
                df = pd.read_csv(fileloc)
                index_fut = ['FUTIDX']
                stk_fut = ['FUTSTK']
                index_opt = ['OPTIDX']
                stk_opt = ['OPTSTK']
                df_index_fut = df.loc[df["INSTRUMENT"].isin(index_fut)]
                df_stk_fut = df.loc[df["INSTRUMENT"].isin(stk_fut)]
                df_index_opt = df.loc[df["INSTRUMENT"].isin(index_opt)]
                df_stk_opt = df.loc[df["INSTRUMENT"].isin(stk_opt)]
                dateobj = datetime.strptime(df_index_fut['TIMESTAMP'].max(),'%d-%b-%Y')
                dateval = datetime.strftime(datetime.strptime(df_index_fut['TIMESTAMP'].max(),'%d-%b-%Y'),'%Y%m%d')
                df_index_fut['dates'] = dateobj
                df_stk_fut['dates'] = dateobj
                df_index_opt['dates'] = dateobj
                df_stk_opt['dates'] = dateobj
                if (self.ficoll.count_documents({"TIMESTAMP": dateval},limit = 1) != 0):
                    logging.error(f"Attempting to load duplicate records for {dateval}")
                    interimmessage = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"date": dateval ,"asset":'Derivatives',"reporttype":"DB Load","statuscode":-100, "statusdesc":f"Records already exists for date {dateval}"}}
                    self.red.publish('loadstatus',json.dumps(interimmessage))
                else:
                    self.ficoll.insert_many(df_index_fut.to_dict('records'))
                    self.fscoll.insert_many(df_stk_fut.to_dict('records'))
                    self.opicoll.insert_many(df_index_opt.to_dict('records'))
                    self.opscoll.insert_many(df_stk_opt.to_dict('records'))
                    logging.info(f"Loaded file {file}")
                    interimmessage = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"date": dateval ,"asset":"Derivatives","reporttype":"DB Load","statuscode":200, "statusdesc":f"Derivatives File {file} loaded successfully."}}
                    self.red.publish('loadstatus',json.dumps(interimmessage))
                os.rename(fileloc,archloc)
                logging.info(f"Moved {file} from {fileloc} to {archloc}")
            except Exception as e:
                logging.error(e)
                interimmessage = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"date": dateval ,"asset":"Derivatives","reporttype":"DB Load","statuscode":-100, "statusdesc":f"{e}"}}
                self.red.publish('loadstatus',json.dumps(interimmessage))
        return json.dumps(interimmessage)

     