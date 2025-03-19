from abc import ABC, abstractmethod
import random 


class PricingStrategy(ABC):

    @abstractmethod
    def calculate_fare(self,base_fare:float,demand:int,supply:int)->float:
        pass 


class SurgePricing(PricingStrategy):

    def calculate_fare(self, base_fare, demand, supply)->float:
        surge_multiplier = max(1.0, min(3.0, demand / max(1, supply)))  # Ensuring it remains reasonable
        return base_fare * surge_multiplier

class NormalPricing(PricingStrategy):

    def calculate_fare(self, base_fare, demand, supply)->float:
        pass 

class PricingManager:

    _instance = None 

    def _initialize(self,strategy:PricingStrategy):
        self.strategy = strategy

    def __new__(cls,strategy:PricingStrategy):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(strategy=strategy)
        return cls._instance
    
    def set_strategy(self,strategry:PricingStrategy):
        self.strategy = strategry

    def calculate_fare(self,base_fare:float,demand:int,supply:int,):
        return self.strategy.calculate_fare(base_fare=base_fare,demand=demand,supply=supply)
    

class Observer(ABC):

    @abstractmethod
    def update(self):
        pass 

class Rider(Observer):

    def __init__(self,name:str):
        self.name = name 

    def update(self,new_fare:float):
        print(f"{self.name} notified: New surge fare is ${new_fare:.2f}")

class Driver(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, new_fare: float):
        print(f"{self.name} notified: New surge fare is ${new_fare:.2f}")

class PriceNotifier:

    def __init__(self):
        self.observers:list[Observer] = []

    def add_observer(self,observer:Observer)->None:
        self.observers.append(observer)

    def remove_observer(self,observer:Observer) -> None:
        self.observers.remove(observer)

    def notify(self,new_fare:float)->None:
        for observer in self.observers:
            observer.update(new_fare)


price_manager = PricingManager(strategy=SurgePricing())
notifier = PriceNotifier()

rider = Rider(name="sohan")
driver = Driver(name="amit")

notifier.add_observer(rider)
notifier.add_observer(driver)

base_fare = 10.0

demand,supply = random.randint(5, 20), random.randint(1, 10)

if demand > supply:
    price_manager.set_strategy(strategry=SurgePricing())
else:
    price_manager.set_strategy(strategry=NormalPricing())

new_fare = price_manager.calculate_fare(base_fare=base_fare,demand=demand,supply=supply)

notifier.notify(new_fare=new_fare)
