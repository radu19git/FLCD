class NonDeterministicException(Exception):
    pass

class State:
    def __init__(self, name, fa):
        self.name = name
        self.fa = fa
        self.transitions = set()

    def add_transition(self, char, to_state):
        for c, second_state in self.transitions:
            if c == char:
                self.fa.is_deterministic = False
                break
        self.transitions.add((char, to_state))

    def get_next_state(self, char):
        if not fa.is_deterministic:
            raise NonDeterministicException()
        for c, second_state in self.transitions:
            if char == c:
                return second_state
        return None

    def __repr__(self):
        return self.name
class FiniteStateMachine:
    def __init__(self):
        self.states = {}
        self.initial = None
        self.finals = set()
        self.is_deterministic = True
        self.alphabet = []

    def add_state(self, state):
        self.states[state.name] = state

    def set_initial(self, state_name):
        self.initial = self.states.get(state_name)

    def add_final(self, state_name):
        self.finals.add(self.states.get(state_name))

    def match_sequence(self, sequence):
        state = self.initial
        for c in sequence:
            if state:
                state = state.get_next_state(c)
            else:
                break
        return state in self.finals



def run_menu(fa):
    while True:
        print("1. Print the set of states\n2. Print the alphabet\n3. Print all the transitions\n"
              + "4. print the set of final states")
        if fa.is_deterministic:
            print("5. Check if sequence is accepted by FA")
        print("0. Exit program")

        x = int(input())
        if x == 0:
            break
        elif x == 1:
            print(', '.join(fa.states.keys()))
        elif x == 2:
            print(', '.join(fa.alphabet))
        elif x == 3:
            for state in fa.states.values():
                for c, second_state in state.transitions:
                    print(f"{state}  -- {c} --> {second_state}")
        elif x == 4:
            print(', '.join(state.name for state in fa.finals))
        elif x == 5:
            sequence = input("Type your sequence: ")
            if fa.match_sequence(sequence):
                print("Sequence is accepted")
            else:
                print("Sequence is not accepted")
        else:
            print("Wrong option")
        input("Press any key to continue...")


def read_fa():
    fa = FiniteStateMachine()
    with open("FA.in", "r") as f:
        lines = f.readlines()
        for state_name in lines[0].split():
            state_name = state_name.strip()
            fa.add_state(State(state_name, fa))

        fa.set_initial(lines[1].strip())
        for state_name in lines[2].split():
            state_name = state_name.strip()
            fa.add_final(state_name)

        fa.alphabet = [c.strip() for c in lines[3].split()]

        for transition_string in lines[4:]:
            transition_array = transition_string.split()
            first_state_name = transition_array[0]
            first_state = fa.states[first_state_name]

            second_state_name = transition_array[1]
            second_state = fa.states[second_state_name]

            for char in transition_array[2:]:
                first_state.add_transition(char, second_state)
    return fa


if __name__ == '__main__':
    fa = read_fa()
    run_menu(fa)
