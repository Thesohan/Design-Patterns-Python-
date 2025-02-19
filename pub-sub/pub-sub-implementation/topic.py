from abc import ABC, abstractmethod
from collections import deque
from threading import Lock
from typing import Any
import time
class ITopic(ABC):

    @abstractmethod
    def subscribe(self,consumer_id:int):
        pass

    @abstractmethod
    def unsubscribe(self,consumer_id:int):
        pass

    @abstractmethod
    def publish(self,message:dict[str,Any]):
        pass

    @abstractmethod
    def consume(self,consumer_id:int):
        pass 

    @abstractmethod
    def reset_offset(self,consumer_id:int,offset:int=0):
        pass 

    @abstractmethod
    def get_consumer_status(self,consumer_id:int):
        pass

class Topic(ITopic):

    def __init__(self,name:str,retention_period:int=60):
        self.name = name
        self.retention_period = retention_period
        self.consumers = {}
        self.messages:deque[tuple[time,str]] = deque()
        self.lock = Lock()

    def subscribe(self,consumer_id:int):
        if consumer_id not in self.consumers:
            self.consumers[consumer_id] = 0

    def unsubscribe(self, consumer_id:int):
        if consumer_id in self.consumers:
            del self.consumers[consumer_id]
    
    def publish(self,message:dict[str,Any]):
        with self.lock:
            self.messages.append((time.time(),message))
        self.__cleanup_old_messages()

    def consume(self, consumer_id):
        with self.lock:
            if consumer_id not in self.consumers:
                raise Exception(f"Consumer {consumer_id} is not subscribed to {self.name}")
            offset = self.consumers[consumer_id]
            if offset < len(self.messages):
                _, message = self.messages[offset]
                self.consumers[consumer_id] += 1
                return message
        return None

    def __cleanup_old_messages(self):
        cutoff = time.time() - self.retention_period
        while self.messages and self.messages[0][0] < cutoff:
            self.messages.popleft()

    def reset_offset(self, consumer_id:int, offset:int = 0):
       if consumer_id in self.consumers:
            self.consumers[consumer_id] = min(offset, len(self.messages))

    def get_consumer_status(self):
        return {c: (self.consumers[c], len(self.messages) - self.consumers[c]) for c in self.consumers}
        