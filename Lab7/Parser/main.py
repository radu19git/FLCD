import traceback

from Grammar import GrammarParser, Grammar
from Parser import LR0Parser, state_as_string, ParseError


def write_to_file(filename, collection):
    with open(filename, "w") as g:
        for state in collection:
            g.write(state_as_string(state) + '\n')

def write_goto_table_to_file(filename, goto_table):
    with open(filename, "w") as g:
        for row in goto_table:
            g.write(str(row) + "\n")

def run_tests():
    with open("g1.test.txt", "r") as f:
        grammar = GrammarParser().parse(f)

    with open("out1.txt", "w") as g:
        parser = LR0Parser(grammar)
        collection = parser.build_canonical_collection()
        write_to_file("g1.colcan.txt", collection)
        try:
            actions, goto_table = parser.build_table(collection)
        except ParseError:
            traceback.print_exc(file=g)
            return
        write_goto_table_to_file("g1.goto_table.txt", goto_table)

        g = open("out1.txt", "w")
        result = parser.parse("bb", actions, goto_table)
        g.write(repr("bb") + ": " + str(result) + "\n")
        try:
            parser.parse("aaaab", actions, goto_table)
            assert False
        except ParseError as e:
            g.write(repr("aaaab") + ": ")
            traceback.print_exc(file=g)

        try:
            parser.parse("baa", actions, goto_table)
        except ParseError:
            g.write(repr("aaaab") + ": ")
            traceback.print_exc(file=g)

def run_working_grammar_tests():
    with open("g3.test.txt", "r") as f:
        grammar = GrammarParser().parse(f)
    with open("out3.txt", "w") as g:
        parser = LR0Parser(grammar)
        collection = parser.build_canonical_collection()
        actions, goto_table = parser.build_table(collection)

        parser.parse("0", actions, goto_table)

def run_toy_language_tests():
    with open("g2.txt", "r") as f:
        grammar = GrammarParser().parse(f)
    with open("out2.txt", "w") as g:
        h = open("p3.txt", "r")
        parser = LR0Parser(grammar)
        collection = parser.build_canonical_collection()
        try:
            actions, goto_table = parser.build_table(collection)
        except ParseError:
            traceback.print_exc(file=g)
            return


        try:
            parser.parse(h.read(), actions, goto_table)
        except ParseError:
            print("alksdjkasjdlaksjdlkaj")
            traceback.print_exc(file=g)

        h.close()
        pass



if __name__ == "__main__":
    run_tests()
    run_working_grammar_tests()
    run_toy_language_tests()