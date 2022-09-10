from abstractFactory.abstract_product import AbstractProductB
from abstract_product import AbstractProductA,AbstractProductB

class ConcreteProductA(AbstractProductA):

    def useful_function_a(self):
        print("concreteProductA implementation of useful function_a")
        return



class ConcreteProductB(AbstractProductB):
    
     def useful_function_b(self):
        print("concreteProductB implementation of useful function_b")
        return