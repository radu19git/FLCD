from hash_table import HashTable, HashTableElement
import re


class SymbolTable(HashTable):
    pass


class ParseError(Exception):
    pass


class ParserElement(HashTableElement):
    pass


class Atom(ParserElement):
    pass


class Symbol(Atom):
    pass


class Operator(Symbol):
    pass


class ArithmeticOperator(Operator):
    pass


class AttributionOperator(Operator):
    pass


class ComparisonOperator(Operator):
    pass


class SquareBracket(Symbol):
    pass


class Parenthesis(Symbol):
    pass


class CurlyBracket(Symbol):
    pass


class Separator(Symbol):
    pass


class Semicolon(Symbol):
    pass


class Type(Symbol):
    pass


class StructureControl(Symbol):
    pass


class IO(Symbol):
    pass


class Identifier(Atom):
    pass


class Constant(Atom):
    pass


class IntConstant(Constant):
    pass


class StringConstant(Constant):
    pass


class Analyser:
    def __init__(self, tokens, sym_table):
        self.__tokens = tokens
        self.__sym_table = sym_table
        self.__sym_count = 0

    def get_atom(self, line):
        matches = [
            (re.match("\+|-|/|\*", line), ArithmeticOperator),
            (re.match(">=|<=|==|!=|<|>", line), ComparisonOperator),
            (re.match("=", line), AttributionOperator),
            (re.match("\[|\]", line), SquareBracket),
            (re.match("\{|\}", line), CurlyBracket),
            (re.match("\(|\)", line), Parenthesis),
            (re.match(";", line), Semicolon),
            (re.match(",", line), Separator),
            (re.match("int|float|char|string", line), Type),
            (re.match("if|while|for", line), StructureControl),
            (re.match("read|write", line), IO),
            (re.match('"[^"]*"', line), StringConstant),
            (re.match("0|([-]?[1-9][0-9]*)", line), IntConstant),
            (re.match("[a-zA-Z_$][a-zA-Z_$0-9]*", line), Identifier),
        ]
        for match, type_ in matches:
            if match is not None:
                return match.group(), type_
        return None, None

    def analyse_line(self, line, line_no):
        line = line.strip()
        pif = []
        while line:
            atom, type_ = self.get_atom(line)
            if atom is None:
                raise ParseError(f"Found invalid atom at line {line_no}; line content: '{line}'")
            identifier_entry = self.__sym_table.get(atom)
            if atom in self.__tokens:
                pif.append(type_(atom, -1))
            else:
                if not identifier_entry:
                    self.__sym_count += 1
                    self.__sym_table.add(atom, type_(atom, self.__sym_count))
                pif.append(self.__sym_table.get(atom))

            line = line[len(atom) :].strip()
        return pif

    def analyse(self, file):
        result = []
        with open(file, "r") as toAnalyse:
            line = toAnalyse.readline()
            line_no = 1
            while line:
                # analizeaza rand cu rand, trebuie sa aiba macar o linie citita la inceput
                result += self.analyse_line(line, line_no)
                line = toAnalyse.readline()
                line_no += 1
        return result


def read_tokens():
    tokens = []
    with open("inputFiles/token.in", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            tokens.append(line)
    return tokens


def print_symbol_table(sym_table):
    print("---- Symbol table ----")
    for item in sym_table.get_all():
        print(f"{item.key:16}    {item.value.value}")
    print("----------------------")


if __name__ == "__main__":
    # creaza tabela de simboluri
    tokens = read_tokens()
    sym_table = SymbolTable()

    # creaza un nou analyser care foloseste se simboluri creata mai devreme
    analyser = Analyser(tokens, sym_table)
    # incepe sa analizeze fisierul
    result = analyser.analyse("inputFiles/p1.txt")

    for token in result:
        print(f"{token.key:16} - value {token.value}")

    print_symbol_table(sym_table)
    pass
