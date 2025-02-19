from abc import ABC, abstractmethod

class IConsumer(ABC):
    @abstractmethod
    def consume(self):
        pass

    @abstractmethod
    def reset_offset(self, offset=0):
        pass

class Consumer(IConsumer):
    def __init__(self, pubsub, topic_name, consumer_id):
        self.pubsub = pubsub
        self.topic_name = topic_name
        self.consumer_id = consumer_id
        topic = self.pubsub.get_topic(self.topic_name)
        if topic:
            topic.subscribe(self.consumer_id)

    def consume(self):
        topic = self.pubsub.get_topic(self.topic_name)
        if topic:
            return topic.consume(self.consumer_id)
        return None

    def reset_offset(self, offset=0):
        topic = self.pubsub.get_topic(self.topic_name)
        if topic:
            topic.reset_offset(self.consumer_id, offset)
