'''
Download and unzip
'''
from dotenv import load_dotenv
import os
from __init__ import getLogger
import dload
import os
import redis
import json

load_dotenv()
logging = getLogger(__name__)

class DownloadandUnzip():
    '''
    This class downloads from NSE website and unzips it to be loaded into Mongo Database
    '''
    def __init__(self) -> None:
        '''
        Initialize the class with the download location
        '''
        self.dataloc = os.getenv("DATA_LOC")
        self.ziploc = os.getenv("ZIP_LOC")
        logging.info(f"Data Location is set to {self.dataloc}")

    def downloadfile(self,url,fil,asset):
        '''
        Download files and save to a location
        '''
        try:
            logging.info(f"Starting download for {url} to file {self.dataloc}/{asset}")
            loc = f"{self.dataloc}/{asset}"
            dload.save_unzip(url,loc)
            logging.info(f"Saving {url} to file {loc}")
            os.rename(fil,f"{self.ziploc}{fil}.zip")
            return 100
        except Exception as e:
            interimmessage = {"action":"loadresponse","payload":{"statuscode":-100, "statusdesc":f"Error Downloading {url} - {asset} to {fil}. Error is {e}"}}
            logging.error(f"Error downloading file {e}")
            return -100