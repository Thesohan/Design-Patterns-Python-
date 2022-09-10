from observable.observable_interface import Observable
class ConcreteObservable(Observable):

    _state = None
    _observers = []

    def attach(self, observer):
        self._observers.append(observer)
        return 

    def detach(self, observer):
        self._observers.remove(observer)
        return 

    def notify(self):
        for observer in self._observers:
            observer.update(self)
        return 

    def setData(self,state):
        self._state=state
        self.notify()
        return 