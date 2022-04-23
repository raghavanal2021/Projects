'''
Action Router - Routes the payload to the appropriate microservices
'''
from asyncore import write
from urllib.robotparser import RequestRate
from __init__ import getLogger
import json, requests,time
from datetime import datetime

logging = getLogger(__name__)
class ActionRouter():
    "Action Router Class routes the payload to the appropriate services"

    def __init__(self):
        #Initialize the action router here
        logging.info("Initializing the Action Router class")
        self.status = ""
    

    def action(self,actioncmd, actionmsg,write_message):
        "Route to the appropriate function"
        default = 'ka'
        return getattr(self,'case_'+actioncmd, lambda:default)(actionmsg,write_message)

    def case_requestload(self,msg,write_message):
        try:
            msgObj = json.loads(msg)
            logging.info(f"Requesting load for {msgObj['startDate']} and {msgObj['endDate']} ")
            r = requests.post("http://localhost:8200/invokeload",json=msgObj)
            if (r.status_code == 200):
                self.status = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"asset":'-','reporttype':'Gateway',"statuscode":r.status_code, "statusdesc": f"Load started for {msgObj['startDate']} and {msgObj['endDate']}"}}
            else:
                self.status = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"asset":'-','reporttype':'Gateway',"statuscode":r.status_code, "statusdesc": f"Load failed to start for {msgObj['startDate']} and {msgObj['endDate']}"}}           
            logging.info(f'Sending to client --> {self.status}')
            write_message('loadresponse',json.dumps(self.status))
        except Exception as e:
            print(e)  
            status = {"action":"loadresponse","payload":{"eventtimestamp":datetime.now().isoformat(),"asset":'-','reporttype':'Gateway',"statuscode":-100, "statusdesc": f"Load failed for {msgObj['startDate']} and {msgObj['endDate']}. Exception is {e}"}}
            write_message('loadresponse',json.dumps(status))