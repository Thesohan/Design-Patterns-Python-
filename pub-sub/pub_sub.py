class Publisher:       

    def subscribe(self,topic,subscriber):
        pass

    def unsubscribe(self,topic,subscriber):
        pass

    def publish(self,topic,message):
        pass 

class Subscriber:
    
    def notify(self,message):
        pass 


class EventPublisher1(Publisher):

    def __init__(self):
        self.subscribers = {}

    def subscribe(self,topic,subscriber):
        if topic not in self.subscribers:
            self.subscribers[topic] = [subscriber]
        else:
            self.subscribers[topic].append(subscriber)

    def unsubscribe(self,topic,subscriber):
        if topic in self.subscribers and subscriber in self.subscribers[topic]:
            self.subscribers[topic].remove(subscriber)

            if len(self.subscribers[topic])==0:
                del self.subscribers[topic]

    def publish(self,topic,message):
        for susbsriber in self.subscribers.get(topic,[]):
            susbsriber.notify(message)


class EvenSuscriber1(Subscriber):

    def __init__(self,name):
        self.name = name

    def notify(self,message):
        print("notified to ",self.name, "message: ",message)


pubSub = EventPublisher1()
subscriber1 = EvenSuscriber1("suscriber 1")
subscriber2 = EvenSuscriber1("suscriber 2")

pubSub.subscribe(topic="topic1",subscriber=subscriber1)
pubSub.subscribe(topic="topic2",subscriber=subscriber2)

pubSub.publish("topic1","hello")

pubSub.publish("topic2","hello2")

pubSub.unsubscribe(topic="topic2",subscriber=subscriber2)


pubSub.publish("topic2","won't reach to subscriber 2")
