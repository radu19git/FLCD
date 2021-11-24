from FA.State import State


class Transition:
    def __init__(self, startState, endState, value):
        self.__startState = State(startState)
        self.__endState = State(endState)
        self.__value = value

    def __repr__(self):
        return f"{self.__startState} ---> {self.__endState} with value {self.__value}"

    @property
    def startState(self):
        return self.__startState
    @property
    def endState(self):
        return self.__endState
    @property
    def value(self):
        return self.__value
    @property
    def as_tuple(self):
        return (self.startState, self.endState, self.value)

    def __eq__(self, other):
        return self.as_tuple == other.as_tuple