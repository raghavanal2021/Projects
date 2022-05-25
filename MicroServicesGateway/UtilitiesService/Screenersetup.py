'''
Setup screener by committing to database
'''
from __init__ import getLogger
from DataRepository import DataRep
import json


logging = getLogger(__name__)

class SetupScreener():
    '''
    Setup a screener
    '''

    def __init__(self) -> None:
        'Initialize the screener'
        logging.info("Screener Setup Started ....")
        self.datarep = DataRep()

    def setScreener(self,contract):
        '''
        Set the screener to the database
        '''
        result = ""
        screenername = contract.screenername
        'Check if the screener exists, if the screener exists dont load. If the screener doesnt exists, load to Mongodb'
        screenerexists = self.datarep.checkscreenerexists(screenername=screenername)
        if (screenerexists):
            result = {"action":"addscreener","payload":{"statuscode":-100, "statusdesc":"Screener Already Exists","return":""}}
        else:
            logging.debug(contract.dict())
            datresult = self.datarep.insertscreenerdata(contract.dict())
            print(datresult)
            r = json.dumps(datresult)
            result = {"action":"addscreener","payload":{"statuscode":100, "statusdesc":"Added Screener successfully", "return":r}}
        return json.dumps(result)

    def getScreener(self):
        datresult = self.datarep.getscreenerdata()
        r = datresult
        result = {"action":"getscreener","payload":{"statuscode":100, "statusdesc":"Screener Fetch successful", "return":r}}
        return json.dumps(result)

    def getenabledScreener(self):
        datresult = self.datarep.getenabledscreener()
        r = datresult
        result = {"action":"getscreener","payload":{"statuscode":100, "statusdesc":"Screener Fetch successful", "return":r}}
        return json.dumps(result)
