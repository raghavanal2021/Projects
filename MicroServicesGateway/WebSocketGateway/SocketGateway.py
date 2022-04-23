'''
This is the Socket Gateway that connects the End of Day modules to the Microservices and the Frontend
'''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import time, json
from __init__ import getLogger
from actionrouter import ActionRouter

#Setup Logging
logger = getLogger(__name__)
#Create a FAST API Application
app = FastAPI()

#Setup CORS
origins = '[*]'
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

#Initialize the Action Router
actionobj = ActionRouter()

#Root Endpoint
@app.get("/")
async def getRoot():
    logger.info("Hitting the Root URL. Things are working fine if you see this message")
    return json.dumps("Status OK. Things are working fine if you see this message")


#Status Check Endpoint
@app.post("/status")
async def status_post(msg:str):
    print(str)


#Setup WebScoketEndpoints
@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:
            "Wait for Data"
            data =  await websocket.receive_text()
            print(data)
            msgcontent = json.loads(data)
            print(msgcontent)
            logger.info(msgcontent)
            await actionobj.action("requestload",data,websocket)
    except WebSocketDisconnect:
        logger.warn("WebSocket Disconnected")