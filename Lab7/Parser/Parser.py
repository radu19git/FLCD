from dataclasses import dataclass

from Grammar import Grammar, Rule, NonTerminal, Terminal, TermParser

def state_as_string(state):
    result = '{'
    for element in state:
        letter, stacks = element
        working, input = stacks
        result += (f"[{letter} -> {''.join(working)}.{''.join(input)}], ")
    result += '}'
    return result

class ShiftAction:
    pass

@dataclass
class ReduceAction:
    production_rule: int

class LR0Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def closure(self, elements):
        result = set(elements)
        while True:
            new_result = set(result)
            for element in result:
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
                                new_element = (input[0], (tuple(), remainder_output))
                                new_result.add(new_element)
            if new_result == result:
                break
            result = new_result
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

    def make_goto_row(self):
        result = {}
        for x in self.grammar.nonterminals + self.grammar.terminals:
            result[x.name] = None
        return result

    def build_canonical_collection(self):
        # [S' -> .S] - S will be the grammar's starting symbol
        # represented as (S' , ((), ('S')), by splitting the production rule in two tuples by the dot
        s0 = self.closure({("S'", (tuple(), (self.grammar.start_symbol.name,)))})
        c = [s0]
        c1 = [s0]
        goto_table = [self.make_goto_row()]
        while True:
            for i, state in enumerate(c):
                for x in self.grammar.nonterminals + self.grammar.terminals:
                    new_state = self.goto(state, x.name)
                    if len(new_state) > 0 and new_state not in c1:
                        print(f"new state = c1[{len(c1)}] = goto(c[{i}], {x.name}) = {state_as_string(new_state)}")
                        goto_table[i][x.name] = len(goto_table)
                        c1.append(new_state)
                        goto_table.append(self.make_goto_row())
            if c1 == c:
                break
            c = c1
        return c, goto_table

    def __element_fully_shifted(self, element):
        nonterm, stacks = element
        working, _input = stacks
        return not _input

    def __count_state_types(self, state):
        fully_shifted = 0
        shiftable = 0
        for element in state:
            if self.__element_fully_shifted(element):
                fully_shifted += 1
            else:
                shiftable += 1
        return fully_shifted, shiftable

    def __validate_state(self, state):
        fully_shifted, shiftable = self.__count_state_types(state)
        if fully_shifted > 0 and shiftable > 0:
            raise ShiftReduceConflict(f"State that contains shiftable and fully shifted elements: {state}")
        if fully_shifted > 1 and shiftable == 0:
            raise ReduceReduceConflict(f"State that contains multiple fully shifted elements: {state}")

    def __is_shift_state(self, state):
        fully_shifted, shiftable = self.__count_state_types(state)
        return fully_shifted == 0 and shiftable > 0

    def __is_reduce_state(self, state):
        fully_shifted, shiftable = self.__count_state_types(state)
        return fully_shifted == 1 and shiftable == 0

    def __convert_to_grammar_rule(self, state) -> Rule:
        [rule] = list(state)
        nonterm, stacks = rule
        working, _input = stacks
        term_parser = TermParser()
        output = [*map(lambda t: term_parser.parse(t), working + _input)]

        return Rule([NonTerminal(nonterm)], [output])

    def build_table(self, collection, goto_table):
        actions = []
        for state in collection:
            self.__validate_state(state)
            if self.__is_shift_state(state):
                actions.append(ShiftAction())
            elif self.__is_reduce_state(state):
                rule = self.__convert_to_grammar_rule(state)
                pn = self.grammar.find_rule(rule)
                if pn < 0:
                    import ipdb
                    ipdb.set_trace()
                actions.append(ReduceAction(pn))

        import ipdb
        ipdb.set_trace()
        return actions


class ShiftReduceConflict(Exception):
    pass


class ReduceReduceConflict(Exception):
    pass
