from abstractFactory.abstract_factory import AbstractFactory
from abstractFactory.concrete_product import ConcreteProductA, ConcreteProductB


class ConcreteFactory1(AbstractFactory):


    def create_product_a(self):
        return ConcreteProductA()


    def create_product_b(self):
        return  ConcreteProductB()


class ConcreteFactory2(AbstractFactory):


    def create_product_a(self):
        return 


    def create_product_b(self):
        return 


