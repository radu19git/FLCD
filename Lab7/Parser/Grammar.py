from dataclasses import dataclass
import re
from typing import List
import string

@dataclass
class Term:
    name: str
    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Term):
            return self.name == other.name

@dataclass
class NonTerminal(Term):
    def __eq__(self, other):
        return super().__eq__(other)

@dataclass
class Terminal(Term):
    def __eq__(self, other):
        return super().__eq__(other)


@dataclass
class Rule:
    input: List[Term]
    outputs: List[List[Term]]

@dataclass
class Grammar:
    nonterminals: List[NonTerminal]
    terminals: List[Terminal]
    start_symbol: NonTerminal
    rules: List[Rule]

    def is_context_free(self):
        for rule in self.rules:
            if len(rule.input) > 1:
                return False
            for term in rule.input:
                if isinstance(term, Terminal):
                    return False
        return True

    def find_rule(self, rule: Rule) -> int:
        production_number = 0
        for r in self.rules:
            if r.input == rule.input:
                pass
            for output in r.outputs:
                production_number += 1
                for out in rule.outputs:
                    if out == output:
                        return production_number
        return -1
class TermParser:
    def parse(self, char: str) -> Term:
        if char.isupper():
            return NonTerminal(char)
        else:
            return Terminal(char)


class RuleParser:
    def __parse_term(self, char: str):
        return TermParser().parse(char)

    def __parse_output(self, sequence):
        return [*map(lambda c: self.__parse_term(c), sequence)]


    def parse(self, line):
        chunks = re.split("->", line)
        lhs = chunks[0].strip()
        rhs = chunks[1].strip()
        separate_outputs = rhs.split("|")
        inputs = [*map(lambda c: self.__parse_term(c), lhs)]
        outputs = [*map(lambda o: self.__parse_output(o.strip()), separate_outputs)]
        return Rule(inputs, outputs)


class GrammarParser:
    def __parse_nonterminals(self, line) -> List[NonTerminal]:
        return [*map(lambda n: NonTerminal(n), line.split())]

    def __parse_terminals(self, line) -> List[Terminal]:
        return [*map(lambda t: Terminal(t), line.split())]

    def __parse_rule(self, line) -> Rule:
        return RuleParser().parse(line)

    def __parse_rules(self, lines) -> List[Rule]:
        return [*map(lambda l: self.__parse_rule(l), lines)]

    def parse(self, file) -> Grammar:
        lines = file.readlines()
        nonterminals = self.__parse_nonterminals(lines[0])
        terminals = self.__parse_terminals(lines[1])
        start_symbol = NonTerminal(lines[2].strip())
        rules = self.__parse_rules(lines[3:])
        return Grammar(nonterminals, terminals, start_symbol, rules)


menu_prompt = """1. Print nonterminals
2. Print terminals
3. Print productions
4. Check if the grammar is context free
0. Exit"""

class Menu:
    def __init__(self, grammar):
        self.grammar = grammar
        self.prompt = menu_prompt

    def run(self):
        while True:
            print(self.prompt)
            opt = int(input(">> "))
            if opt == 0:
                break
            if opt == 1:
                print(', '.join(map(lambda n: n.name, self.grammar.nonterminals)))
            elif opt == 2:
                print(', '.join(map(lambda t: t.name, self.grammar.terminals)))
            elif opt == 3:
                for rule in self.grammar.rules:
                    print(rule)
            elif opt == 4:
                if self.grammar.is_context_free():
                    print("Is context free")
                else:
                    print("Not context free")
            input("\nPress any key to continue...")

def test():
    with open("g1.test.txt", "r") as f:
        assert NonTerminal('1') == NonTerminal('1')
        grammar = GrammarParser().parse(f)
        assert grammar.nonterminals
        assert grammar.terminals
        assert grammar.start_symbol in grammar.nonterminals
        for term in grammar.nonterminals + grammar.terminals:
            assert isinstance(term, Term)
            assert term.name
        assert grammar.rules
        for rule in grammar.rules:
            assert rule.input
            assert rule.outputs
            for output in rule.outputs:
                for term in output:
                    assert isinstance(term, Term)
        assert grammar.is_context_free()

    print("passed")


if __name__ == '__main__':
    test()
    with open("g1.test.txt", "r") as f:
        grammar = GrammarParser().parse(f)
        Menu(grammar).run()
