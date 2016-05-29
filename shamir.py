from Crypto.Util import number
import numpy as np

# target = the secret to be split
# n = number of shares of the secret wanted
# k = minimum of values needed to reconstruct the secret

def getShares(target, n, k):
    coefs = []
    shares = []
    coefs.append(target) # secret is f(0)
    for i in range(k):
        coefs.append(number.getRandomInteger(16))
    npoly = np.poly1d(coefs)
    for i in range(1, n):
        print i
        shares.append((i,npoly(i)))
        print shares[i-1]
    return shares

def computeDifs(current, shares):
    diff = 1 # current = (point, share)
    for index in range(len(shares)):
        if shares[index][0] != current[0]:
            diff = diff * (current[0] - shares[index][0])
    print "diff is ",diff
    return diff

# return SUM(PRODUCTS(n)) from roots
# useful for Viete's formulas
def partialSumOfN(roots, n, i=0):
    rsum = 0
    for i in range(len(roots) - n):
        aux = 1
        for j in range(i,i+n):
            aux = aux * roots[j][0]
        rsum + aux
    return rsum

def getSecret(shares):
    # construct a polynom with Lagrange Interpolation
    # f(x) = SUM(yi, lagrangepol(x))
    # lagrangepol(x) of degree (k -1) 
    coefs = [0] * len(shares)

    for i in range(len(shares)):
        dif = computeDifs(shares[i], shares)
        coefi = partialSumOfN(shares, len(shares) - i)
        print coefi
        if (len(shares) -i) % 2 :
            coefi  = (-1)*coefi
        coefs[i] = coefs[i] + float (coefi * shares[i][1] / dif)
    print coefs

sh = getShares(1234, 7, 3)
print "shares are ",sh
computeDifs(sh[0], sh)
getSecret(sh)

















