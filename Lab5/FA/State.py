class State:
    def __init__(self, name):
        self.__name = name

    def __repr__(self):
        return f"{self.__name}"

    def __eq__(self, other):
        return self.__name == other.__name

    def getName(self):
        return self.__name
