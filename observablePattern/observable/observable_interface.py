from abc import ABC,abstractmethod
class Observable(ABC):

    @abstractmethod
    def attach(self,observer):
        pass

    @abstractmethod
    def detach(self,observer):
        pass

    @abstractmethod
    def notify(self):
        pass

    @abstractmethod
    def setData(self):
        pass
