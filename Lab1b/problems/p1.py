nb1 = int(input('Choose a number'))
nb2 = int(input('Choose a number'))
nb3 = int(input('Choose a number'))

min = 5000

if nb1 <= nb2:
    if nb1 <= nb3:
        min = nb1
    else:
        min = nb3
else:
    if nb2 <= nb3:
        min = nb2
    else:
        min = nb3