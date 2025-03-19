"""
--> You are working for a ride-sharing company that needs to optimize its pricing strategy to increase revenue.
Your task is to design and implement a system that calculates optimal ride prices based on various factors such as time of day, distance, demand. 
The system should also allow for dynamic adjustments to pricing in real-time.

Task:
Write an object-oriented program in your preferred language that implements the ride-sharing company's pricing algorithm.
Your program should include the following classes:
Ride: Represents a single ride, with properties such as distance, time of day, demand, and price.
Driver
Rider

PricingAlgorithm: Represents the pricing algorithm, with methods for determining the optimal price for a given ride based on its properties.
distanceMultiplier, timeOfDayMultipliers, demandMultipliers are pre-calculated
Your program creates Ride objects for each ride, passes them to the PricingAlgorithm to determine the optimal price, and outputs the final price for each ride.
"""
from uuid import uuid4
from enum import Enum
from abc import ABC, abstractmethod




MAXIMUM_PRICE = 1000000000000

class DayTime(Enum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4

class Demand(Enum):
    HIGH = 1
    LOW = 2
    MEDIUM = 3


TIME_OF_THE_DAY_MULTIPLIER = {
    DayTime.AFTERNOON : 1,
    DayTime.EVENING : 2,
    DayTime.MORNING : 3,
    DayTime.NIGHT : 4
}

TIME_OF_THE_DAY_MULTIPLIER = {
    DayTime.AFTERNOON : 1,
    DayTime.EVENING : 2,
    DayTime.MORNING : 3,
    DayTime.NIGHT : 4
}


DEMAND_MULTIPLIER = {
    Demand.HIGH: 3,
    Demand.LOW: 1,
    Demand.MEDIUM : 2
}

DISTANCE_MULTIPLIER = {
    10: 3,
    100: 2,
    1000000000: 1
}

class PricingAlgoType(Enum):

    DYNAMIC_PRICING_ALGO = 1


class Rider:

    def __init__(self,name:str,):
        self.name = name
        self.id = str(uuid4())

class Driver:

    def __init__(self,name:str,):
        self.name = name
        self.id = str(uuid4())

class Ride:
    def __init__(self,rider:Rider,distance:int,day_time:DayTime,demand:Demand=None,price:float=None):
        self.distance = distance
        self.day_time  = day_time
        self.demand = demand
        self.price = price
        self.rider = rider
        self.driver = None

    def set_driver(self,driver:Driver)->None:
        self.driver = driver

class IPricingAlgorithm(ABC):
    _registry:dict[PricingAlgoType,"IPricingAlgorithm"] = {}

    @classmethod
    def register(cls,pricing_algo_type:PricingAlgoType,algorithm:"IPricingAlgorithm")->None:
        cls._registry[pricing_algo_type] = algorithm

    @classmethod
    def get_pricing_algorithm(cls,pricing_algo_type:PricingAlgoType)->"IPricingAlgorithm":
        if pricing_algo_type in cls._registry:
            return cls._registry[pricing_algo_type]
        raise ValueError(f"pricing algo doesn't exist: {pricing_algo_type}")

    
    @abstractmethod
    def calculate_price(self,ride:Ride)->float:
        pass 

class DynamicPricingAlog(IPricingAlgorithm):


    def calculate_price(self,ride:Ride)->float:
        distance = ride.distance
        if distance > 10:
            distance_multplier = DISTANCE_MULTIPLIER.get(10)
        elif distance < 100:
            distance_multplier = DISTANCE_MULTIPLIER.get(100)
        else:
            distance_multplier = DISTANCE_MULTIPLIER.get(1000000000)

        final_price = ride.price + min(ride.price+MAXIMUM_PRICE, ride.price * distance_multplier * TIME_OF_THE_DAY_MULTIPLIER.get(ride.day_time) * DEMAND_MULTIPLIER.get(ride.demand))
        return final_price
    
IPricingAlgorithm.register(PricingAlgoType.DYNAMIC_PRICING_ALGO,DynamicPricingAlog)



"""
Your program creates Ride objects for each ride, passes them to the PricingAlgorithm to determine the optimal price, and outputs the final price for each ride.
"""

if __name__ == "__main__":
    rider  = Rider(name="sohan")

    driver = Driver(name="Kathait")

    ride = Ride(rider=rider,distance=10001,day_time=DayTime.NIGHT,demand=Demand.HIGH,price=10)
    pricing_algo:IPricingAlgorithm  = IPricingAlgorithm.get_pricing_algorithm(pricing_algo_type=PricingAlgoType.DYNAMIC_PRICING_ALGO)()
    print(pricing_algo.calculate_price(ride=ride))



"""
EVENING, 10, HIGH , 100 ===> 1300
11 ---> 1900
MORNING ---> 2800

low --> 1000
101 ---> 1000

10001, NIGHT, HIGH, PRICE 10--> 370

"""