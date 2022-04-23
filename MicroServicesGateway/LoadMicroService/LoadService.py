'''
Load Microservice
'''
from fastapi import Response
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher
from __init__ import getLogger
from nameko.web.handlers import http
import pika
import redis,json
from datetime import datetime
import threading

logging = getLogger(__name__)
class LoadService:
    #Service Class for Loader
    name = "service_loader"

    red = redis.StrictRedis('localhost',6379,charset='utf-8', decode_responses=True)
    dispatch = EventDispatcher()
    
 #   def genuid(uid):
 #       if getattr(uid, "uid", None) is None:
 #           uid.tid = threading.current_thread().ident
 #           uid.uid = 0
 #           uid.uid += 1
 #       return ("LDRQST" + str(uid.tid + uid.uid))


    @http('POST','/invokeload')
    def invoke_load(self,request):
        inp_contract = request.get_data(as_text = True)
        print("Received : " + request.get_data(as_text = True))
        try:
            #uid = threading.local()
            req_id =  1
            logging.info(f"Request ID is {req_id}.")
            inp_obj = json.loads(str(inp_contract))
            logging.info(f"Passing {inp_obj['assetClass']} to appropriate Services. ")
            for assets in inp_obj['assetClass']:
                if (assets == 'EQ'):
                    interimmessage = {"action":"loadresponse","payload":{"requestid": req_id,"eventtimestamp":datetime.now().isoformat(),"date":f"{inp_obj['startDate']}-{inp_obj['endDate']}" ,"asset":",".join(inp_obj['assetClass']),"reporttype":",".join(inp_obj['options']),"statuscode":200, "statusdesc":"Passed on to equity Load."}}
                    self.dispatch_data('equityload',inp_contract)
                    self.red.publish('loadstatus',json.dumps(interimmessage))
                if (assets == 'FUT'):
                    interimmessage = {"action":"loadresponse","payload":{"requestid": req_id,"eventtimestamp":datetime.now().isoformat(),"date":f"{inp_obj['startDate']}-{inp_obj['endDate']}" ,"asset":",".join(inp_obj['assetClass']),"reporttype":",".join(inp_obj['options']),"statuscode":200, "statusdesc":"Passed on to Derivatives Load."}}
                    self.dispatch_data('derivload',inp_contract)
                    self.red.publish('loadstatus',json.dumps(interimmessage))
        except Exception as e:
            logging.error(e)
        return json.dumps(interimmessage)


    @rpc
    def dispatch_data(self,channel,inp_contract):
            self.dispatch(channel,inp_contract)
