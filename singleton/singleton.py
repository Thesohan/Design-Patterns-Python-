from cmath import log


class Singleton:
    """
    This pattern restricts the instantiation of a class to one object. It is a type of creational pattern and involves
    only one class to create methods and specified objects.
    """

    __instance=None

    def __init__(self):
        """Vertually private constructor"""
        if self.__instance is not None:
            raise Exception("This class is singleton, Please call get_instance instead.")
        else:
            Singleton.__instance=self

    @staticmethod
    def get_instance():
        if Singleton.__instance is None:
            return Singleton()
        return Singleton.__instance

# It will raise exception
# s = Singleton()
# print(s)

s = Singleton()
print(s)

s = Singleton()
print(s)