from __future__ import annotations
from abc import ABC,abstractmethod


class AbstractFactory(ABC):

    @abstractmethod
    def create_product_a(self):
        pass

    @abstractmethod
    def create_product_b(self):
        pass