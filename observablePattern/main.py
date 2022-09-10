from observable.concrete_observable import ConcreteObservable
from observers.concrete_observer_a import ConcreteObserverA
from observers.concrete_observer_b import ConcreteObserverB

if __name__ == '__main__':
    observable = ConcreteObservable()
    
    observer_a = ConcreteObserverA()
    observable.attach(observer_a)

    observer_b = ConcreteObserverB()
    observable.attach(observer_b)

    observable.setData(10)
    observable.setData(11)

    observable.detach(observer_a)

    observable.setData(90)