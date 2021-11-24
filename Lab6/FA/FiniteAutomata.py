from typing import List

from FA.State import State
from FA.Transition import Transition

class FA:

    def __init__(self, fileName):
        self.__states = []
        self.__transitions = []
        self.__finalStates = []
        self.__alphabet = []

        f = open(fileName, "r")
        lines = f.readlines()

        state = State(lines[0].strip('\n'))
        self.__initialState = state
        self.__states.append(self.__initialState)

        for stateName in lines[1].split(' '):
            state = State(stateName.strip('\n'))
            self.__states.append(state)

        for finalStateName in lines[2].split(' '):
            state = State(finalStateName.strip('\n'))
            self.__finalStates.append(state)

        for alphabetToken in lines[3].split(' '):
            token = State(alphabetToken.strip('\n'))
            self.__alphabet.append(token)
        self.__alphabet.append(' ')

        for i in range(4, len(lines)):
            line = lines[i]
            lineTransitions = line.split(' ')
            transition = Transition(lineTransitions[0].strip('\n'),
                                    lineTransitions[1].strip('\n'),
                                    lineTransitions[2].strip('\n'))
            self.__transitions.append(transition)
        f.close()

    def getAlphabet(self):
        return self.__alphabet

    def getStates(self):
        return self.__states

    def getInitialState(self):
        return self.__initialState

    def getFinalStates(self):
        return self.__finalStates

    def getTransitions(self):
        return self.__transitions

    def accepts(self, s: List[str]):
        q = self.__initialState
        for token in s:
            found = False
            for transition in self.__transitions:
                if transition.startState == q and transition.value == token:
                    q = transition.endState
                    found = True
            if not found:
                return False
        if q in self.__finalStates:
            return True
        return False

