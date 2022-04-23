import redis
from __init__ import getLogger

logging = getLogger(__name__)

class DataListener():

    def __init__(self) -> None:
        self.red = redis.StrictRedis('localhost',6379,charset='utf-8', decode_responses=True)
        print("Started the Listener...")
        self.sub = self.red.pubsub()
        self.sub.subscribe('loadstatus')
        


    def subscribeandSend(self,io):
        for message in self.sub.listen():
            if message is not None and isinstance(message,dict):
                msg = message.get('data')
                io.emit('loadresponse',msg)
        return None