from argparse import Action
from concurrent.futures import thread
from flask import Flask;
from flask_socketio import SocketIO, emit
from actionrouter import ActionRouter;
import json
import threading
from Listener import DataListener
import eventlet



#Create App using Flask
app = Flask(__name__)
eventlet.monkey_patch()

#Create a Server and fix CORS
socketIO = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

#Set the debug
app.debug = True

#Set to localhost
app.host = 'localhost'  
app.port = 8000

actionObj = ActionRouter()

@socketIO.on("requestload")
def handle_load_request(msg):
    msgobj = json.loads(msg)
    actionObj.action('requestload',msg,emit)   
    return None    

    
if __name__ == '__main__':

    listen = DataListener()
    listenerthread = threading.Thread(target=listen.subscribeandSend,args=[socketIO])
    listenerthread.start()  
    socketIO.run(app, debug=True, port=8000)

 