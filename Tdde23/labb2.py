import math

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def dsum(num, mult):
    total = 0
    sum = num * mult
    list_of_num = [int(x) for x in str(sum)]
    for i in list_of_num:
        total += i
    return total

def check_pnr(pnr):
    total = 0
    for i in range(len(pnr) - 1):
        if i % 2 != 0:
            mult = 1
        else:
            mult = 2
        total += dsum(pnr[i], mult)
    return (roundup(total) - total) == pnr[9]