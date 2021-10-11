from hash_table import HashTable, HashTableElement


class SymbolTable(HashTable):
    pass
    # asa? Vrea neaparat sa ii zica SymbolTable si nu structura de date


class ParserElement(HashTableElement):
    pass


class Atom(ParserElement):
    pass


class Symbol(ParserElement):
    pass


class Analyser:
    def __init__(self, tokens):
        self.__atoms_table = atoms_table
        self.__sym_table = sym_table



    def analyse(self):
        toAnalyse = open("p1.txt", "r")
        line = toAnalyse.readline()
        # input: p.txt and token.in
        # analyze char by char and split by separators and operators
        # complete Program Internal Form (PIF) with all lexical elements, specifying if they
        # belong in the Symbol Table or if they are a keyword
        # In the Symbol Table we have the identifiers and the constants
        # We also check for lexical errors
        while line:
            pass


def make_tokens():
    tokens = SymbolTable()
    with open("token.in", "r") as f:
        lines = f.readlines()
        for line in lines:
            tokens.add(line, Symbol())
    return tokens


if __name__ =="__main__":
    self.__tokens = []
    f = open("token.in", "r")

    f.close()
    tokens = SymbolTable()

    #analyser = Analyser()
    pass