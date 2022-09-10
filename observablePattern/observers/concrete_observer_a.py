from observers.observer_interface import ObserverInterface

class ConcreteObserverA(ObserverInterface):

    def update(self,subject):
        print(subject)
        print("ConcreteObserverA responded to the event")



