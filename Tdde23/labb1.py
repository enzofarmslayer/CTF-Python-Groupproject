def div_by_three(n):
    div = n / 3
    return div == int(div)


def max2(x, y):
    if (x > y):
        return x
    return y

def max3(x, y, z):
    first = max2(x, y)
    second = max2(first, z)
    return max2(first, second)

def max(*numbers):
    ev = numbers[0]
    for num in numbers:
        if (ev < num):
            ev = num
    return ev

