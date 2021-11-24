from Grammar import Grammar

def state_as_string(state):
    result = '{'
    for element in state:
        letter, stacks = element
        working, input = stacks
        result += (f"[{letter} -> {''.join(working)}.{''.join(input)}], ")
    result += '}'
    return result


class LR0Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def closure(self, elements):
        result = set(elements)
        for element in elements:
            nonterm, stacks = element
            working, input = stacks
            if not input:
                continue
            if input[0] in self.grammar.nonterminals:
                for rule in self.grammar.rules:
                    if rule.input[0] == input[0]:
                        # add incoming production rules formed with the symbol right after the dot (in the input/second stack)
                        for output in rule.outputs:
                            remainder_output = tuple(map(lambda t: t.name, output))
                            result.add((input[0], (tuple(), remainder_output)))
        return result

    def goto(self, state, X):
        shifted_elements = set()       # shifted means that the elements in an LR item  [A -> aB.c]
                                        # will become [A -> a.Bc] (will be consumed and appended on the stack)
        for element in state:
            nonterm, stacks = element
            working_stack, input_stack = stacks
            if not input_stack or input_stack[0] != X:
                continue
            shifted_elements.add((
                nonterm,
                (working_stack + (input_stack[0],), input_stack[1:]) # shift from right to left of dot
            ))
        return self.closure(shifted_elements)

    def build_canonical_collection(self):
        # [S' -> .S] - S will be the grammar's starting symbol
        # represented as (S' , ((), ('S')), by splitting the production rule in two tuples by the dot
        s0 = self.closure({("S'", (tuple(), (self.grammar.start_symbol.name,)))})
        c = [s0]
        c1 = [s0]
        while True:
            for i, state in enumerate(c):
                for x in self.grammar.nonterminals + self.grammar.terminals:
                    new_state = self.goto(state, x.name)
                    if len(new_state) > 0 and new_state not in c1:
                        print(f"new state = c1[{len(c1)}] = goto(c[{i}], {x.name}) = {state_as_string(new_state)}")
                        c1.append(new_state)
            if c1 == c:
                break
            c = c1
        return c

