'''
Screener Gateway
'''
from fastapi import Response
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher
from __init__ import getLogger
from nameko.web.handlers import http
import redis,json
from datetime import datetime
import requests

logging = getLogger(__name__)
class ScreenerService:
    #Service Class for Loader
    name = "service_screener"

    red = redis.StrictRedis('localhost',6379,charset='utf-8', decode_responses=True)
    dispatch = EventDispatcher()
    
 #   def genuid(uid):
 #       if getattr(uid, "uid", None) is 
    @http('POST','/invokeload')
    def invoke_screener(self,request):
        req_id =  1
        logging.info(f"Request ID is {req_id}.")
        returnobj = ""
        input = request.get_data(as_text = True)
        print(input)
        inputobj = json.loads(input)
        screendate = inputobj['date']
        type = inputobj['type']
        screenerslist = json.loads(self.enabledscreeners())
        for screeners in screenerslist:
            print(screeners['screenertype'])
            screentype = screeners['screenertype']
            self.dispatch(screentype,input)
            interimmessage = {"action":"loadresponse","payload":{"requestid": req_id,"eventtimestamp":datetime.now().isoformat(),"date":f"{screendate}" ,"asset":inputobj['type'],"reporttype":"Screener","statuscode":200, "statusdesc":f"Starting {screentype} for {screendate} - {type}"}}
            self.red.publish('loadstatus',json.dumps(interimmessage))
        #TODO : Find a good return contract
        finalmessage = {"action":"InvokeScreener","payload":{"request_id": req_id, "eventtimestamp":datetime.now().isoformat(),"asset":type,"statuscode":200, "statusdesc":"Invoke load successfully completed."}}
        return json.dumps(finalmessage)
 


    def enabledscreeners(self):
        r = requests.get("http://localhost:8400/enabledscreeners")
        l = eval(json.loads(json.dumps(r.text)))
        logging.debug(l)
        enabledscreeners = json.loads(l)        
        returnobj = enabledscreeners['payload']['return']
        return json.dumps(returnobj)
