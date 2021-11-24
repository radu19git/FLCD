# Max of 3 numbers

nb1 = 1
nb2 = 2
nb3 = 3

max = 0

if nb1 >= nb2:
    if nb1 >= nb3:
        max = nb1
    else:
        max = nb3
else:
    if nb2 >= nb3:
        max = nb2
    else:
        max = nb3