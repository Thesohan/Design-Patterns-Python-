from threading import Lock 
from topic import Topic
from publisher import Publisher
from consumer import Consumer
class PubSubSystem:
    def __init__(self):
        self.topics = {}
        self.lock = Lock()

    def create_topic(self, topic_name, retention_period=60):
        with self.lock:
            if topic_name not in self.topics:
                self.topics[topic_name] = Topic(topic_name, retention_period)

    def delete_topic(self, topic_name):
        with self.lock:
            if topic_name in self.topics:
                del self.topics[topic_name]

    def get_topic(self, topic_name):
        return self.topics.get(topic_name)

# Example Usage
if __name__ == "__main__":
    pubsub = PubSubSystem()
    pubsub.create_topic("news")

    publisher = Publisher(pubsub, "news")
    consumer1 = Consumer(pubsub, "news", "consumer_1")
    consumer2 = Consumer(pubsub, "news", "consumer_2")

    publisher.publish("Breaking news 1")
    publisher.publish("Breaking news 2")

    print(consumer1.consume())  # Breaking news 1
    print(consumer2.consume())  # Breaking news 1
    print(consumer1.consume())  # Breaking news 2
    print(consumer2.consume())  # Breaking news 2

    print(pubsub.get_topic("news").get_consumer_status())
