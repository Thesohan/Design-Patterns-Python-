from abc import abstractmethod,ABC

class IPublisher(ABC):
    @abstractmethod
    def publish(self, message):
        pass

class Publisher(IPublisher):
    def __init__(self, pubsub, topic_name):
        self.pubsub = pubsub
        self.topic_name = topic_name

    def publish(self, message):
        topic = self.pubsub.get_topic(self.topic_name)
        if topic:
            topic.publish(message)


