%{

#include <stdio.h>

%}

%option noyywrap

DIGIT [0-9]

%%

("-"|"+")?{DIGIT}+ {
    printf("digit %s \n", yytext);
}

%%

int main() {
    yyin = fopen("digits.in", "r");
    printf("merge\n");
    if (!yylex()) {
        printf("Parse successful\n");
    }
    return 0;
}