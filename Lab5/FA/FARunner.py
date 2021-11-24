from typing import List, Tuple
from string import ascii_lowercase, ascii_uppercase, ascii_letters, digits

# q0 goes to q1a q1b ... and all the other possible combinations
from Analyser.Analyser import Analyser
from FA import FiniteAutomata


def generate_FA():
    final_states = [
        f'q1_{ch}' for ch in digits + ascii_letters
    ]

    states = ['q0'] + final_states

    transitions: List[Tuple[str]] = []

    for digit in ascii_letters:
        transitions.append(
            (
                f'q0',
                f'q1_{digit}',
                digit
            ))

    for digit in digits + ascii_letters:
        for other_digit in digits + ascii_letters:
            transitions.append(
                (
                    f'q1_{digit}',
                    f'q1_{other_digit}',
                    other_digit
                ))

    # for a int constant, we can either go directly to 0
    transitions.append(
        ('q0', 'q2_0f', '0')
    )
    states.append('q2_0f')
    final_states.append('q2_0f')

    # for any int that doesn''t start with 0

    # first from q0 to q2_digit
    for digit in digits[1:]:
        transitions.append(
            (
                f'q0',
                f'q2_{digit}',
                digit
            ))

    # the second third etc digits

    for digit in digits:
        for other_digit in digits:
            transitions.append(
                (
                    f'q2_{digit}',
                    f'q2_{other_digit}',
                    other_digit
                ))
    states += [f'q2_{digit}' for digit in digits]
    final_states += [f'q2_{digit}' for digit in digits]

    f = open("FA.in", "w")
    f.writelines([
        'q0\n',
        ' '.join(states),
        '\n',
        ' '.join(final_states),
        '\n',
        ' '.join(ascii_letters + digits),
        '\n',
        '\n'.join([' '.join(transition) for transition in transitions])
    ])
    f.close()


# generate_FA()
#
# fa = FA('FA.in')
#
# test = [
#     ['1', '2', '3'],
#     ['1'],
#     ['0'],
#     ['a', '2', '3'],
#     ['a', 'b', 'c'],
#     ['Z'],
#     # not OK:
#     ['2', 'b', 'c'],
#     ['0', '1'],
# ]
# for seq in test:
#     print(fa.accepts(seq))


from pprint import pprint as pp
analyser = Analyser()
print('asdf\\n'.rstrip())
pp(analyser.getTokens())
analyser.analyse()
pp(analyser.getPIF())
analyser.printST()
pp(analyser.getST())
