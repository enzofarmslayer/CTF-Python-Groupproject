import sys
sys.setrecursionlimit(2000)

# def bs(n, k, memo={}):
#     if k == n or k == 0:
#         return 1
#     elif k > n:
#         return 0
#     elif (n, k) in memo:
#         return memo[(n, k)]
#     else:
#         result = bs(n-1, k-1, memo) + bs(n-1, k, memo)
#         memo[(n, k)] = result
#         return result
# print(bs(1000, 800))

def bs(n, k):
    if k == n or k == 0:
        return 1
    elif k > n:
        return 0
    else:
        result = bs(n-1, k-1) + bs(n-1, k)
        return result
print(bs(1000, 1))