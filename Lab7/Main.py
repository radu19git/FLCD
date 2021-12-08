from Analyser.Analyser import Analyser
from FA.FiniteAutomata import FA
from FA.State import State


def printMenu():
    print('1 - set of States')
    print('2 - alphabet')
    print('3 - transitions')
    print('4 - final States')
    print('5 - exit')

fa = FA('FA/Fa.simple.in')
# print(fa.getInitialState())
# print(fa.getFinalStates())
# print(fa.getTransitions())

# testSequence = input("Give test sequence: ")
inputs = [
    'a b b c'.split(),  # not OK
    'a b a c'.split(),  # OK
    'a c'.split()  # not OK
]
for inputToken in inputs:
    if fa.accepts(inputToken):
        print(inputToken, 'ÓK')
    else:
        print(inputToken ,'not ok')


choice = ""
while choice != 5:
    printMenu()
    choice = int(input())
    if choice == 1:
        print(fa.getStates())
    elif choice == 2:
        print(fa.getAlphabet())
    elif choice == 3:
        print(fa.getTransitions())
    elif choice == 4:
        print(fa.getFinalStates())
    elif choice == 5:
        break
