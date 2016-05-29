from Crypto.Util import number
import numpy as np
from operator import mul

# target = the secret to be split
# n = number of shares of the secret wanted
# k = minimum of values needed to reconstruct the secret

def getShares(target, n, k):
    coefs = []
    shares = []
    for i in range(k - 1):
        coefs.append(number.getRandomInteger(8))
    coefs.append(target) # secret is f(0)
    npoly = np.poly1d(coefs)
    print npoly
    print "Secret is", npoly(0)
    for i in range(1, n):
        shares.append((i, npoly(i)))
    return shares

def computeDifs(current, shares):
    diff = 1 # current = (point, share)
    for index in range(len(shares)):
        if shares[index][0] != current[0]:
            diff = diff * (current[0] - shares[index][0])
    return diff

# return SUM(PRODUCTS(n)) from roots
# useful for Viete's formulas
def partialSumOfN(roots, n):
    rsum = 0
    for i in range(len(roots) - n + 1):
        aux = 1
        for j in range(i,i+n):
            aux = aux * roots[j][0]
        rsum = rsum + aux
    return rsum


def product(roots):
    return reduce(lambda mul, (x,y): mul * x, roots, 1)

# Use Lagrange Interpolation to find the initial polynom
# Each x of the shares is a root for the ecuation.
def getSecret(shares):
    secret = 0
    P = product(shares)
    for i in range(len(shares)):
        dif = computeDifs(shares[i], shares)
        aux = (P / shares[i][0])
        if ((len(shares) - 1) % 2) == 1 :
            aux = aux * (-1)
        aux = float (aux * shares[i][1] / dif)
        secret = secret + aux
    return secret

sh = getShares(1234, 7, 3)
print "shares are ",sh[0:3]
print "---Test Product --"
print product(sh[0:3])
print "---Test Decomposition--"
print getSecret(sh[0:3])

