from observers.observer_interface import ObserverInterface

class ConcreteObserverB(ObserverInterface):

    def update(self,subject):
        print(subject)
        print("ConcreteObserverB responded to the event")



