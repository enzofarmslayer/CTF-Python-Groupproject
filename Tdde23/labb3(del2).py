import sys
sys.setrecursionlimit(2000)

def choose(n, k, memo={}):
    if k == n or k == 0:
        return 1
    elif k > n:
        return 0
    elif (n, k) in memo:
        return memo[(n, k)]
    else:
        result = choose(n-1, k-1, memo) + choose(n-1, k, memo)
        memo[(n, k)] = result
        return result
# print(choose(1000, 4))

# def bs(n, k):
#     if k == n or k == 0:
#         return 1
#     elif k > n:
#         return 0
#     else:
#         result = bs(n-1, k-1) + bs(n-1, k)
#         return result
# print(bs(1000, 3))

import decimal

def nfact(n):
  if n == 0:
    return 1
  else:
    return n* nfact(n-1)
  
def bs(n, k):
  result = nfact(n) // (nfact(k) * int((nfact(n - k))))
  return result

# print(bs(1000, 4))

x = 1000
y = 800

print(bs(x, y) == choose(x, y))
print(bs(x, y))
print(choose(x, y))

  