from BST.BST import BST, DuplicateError
import re
import string
from FA.FiniteAutomata import FA

class LexicalError(Exception):
    pass

class Analyser:
    def __init__(self):
        self.__ST = BST()
        self.__PIF = []
        self.__separators = ['{', '}', '[', ']', ';', ' ']
        self.__operators = ['+', '-', '*',  '/',  ':',  '<', '<=', '=', '>=', '>']

        self.__tokens = []

        self.__FA = FA("FA.in")

        f = open("C:/Users/flutu/OneDrive/Desktop/FLCD/FLCD/Lab4/LanguageStructure/token.in", "r")
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            self.__tokens.append(line)
        f.close()

    def genPIF(self, token, st_position):
        self.__PIF.append([token, st_position])

    def checkIndentifier(self, token):
        pattern = re.compile("^[a-zA-Z]+[0-9]*$")
        return pattern.match(token)
        # self.__FA.accepts(token)

    def checkConstant(self, token):
        int_const_re = "0|([1-9][0-9]*)$"
        str_const_re = '"[^"]*"$'  # a string that contains anything except "
        pattern = re.compile(f'({int_const_re})|({str_const_re})')
        return pattern.match(token)
        # self.__FA.accepts(token)

    def analyse(self):

        # input: p.txt and token.in
        # analyze char by char and split by separators and operators
        # complete Program Internal Form (PIF) with all lexical elements, specifying if they
        # belong in the Symbol Table or if they are a keyword
        # In the Symbol Table we have the identifiers and the constants
        # We also check for lexical errors

        toAnalyse = open("C:/Users/flutu/OneDrive/Desktop/FLCD/FLCD/Lab4/LanguageStructure/p1.txt", "r")
        line = toAnalyse.readline()
        line_number = 1
        while line:
            line = line.strip()
            words = re.split("(>=|<=|!=|<|>|=|\{|\}|\[|\]|\{|\}|;|:|\+|\*|/|-|\(|\)| |,)", line)
            for word in words:
                if not word:
                    continue
                if word in self.__tokens:
                    if word != " ":
                        self.genPIF(word, -1)
                else:
                    # if self.checkIndentifier(word) or self.checkConstant(word):
                    if self.__FA.accepts(word):
                        try:
                            index = self.__ST.insertBST(word)
                            self.genPIF(word, index)
                        except DuplicateError as e:  #
                            pass
                    else:
                        raise LexicalError(f"Error at line {line_number}: invalid word detected: '{word}'")
            line = toAnalyse.readline()
            line_number += 1

    def getPIF(self):
        return self.__PIF

    def getST(self):
        return self.__ST.getBST()

    def printST(self):
        self.__ST.printBST()

    def getTokens(self):
        return self.__tokens

