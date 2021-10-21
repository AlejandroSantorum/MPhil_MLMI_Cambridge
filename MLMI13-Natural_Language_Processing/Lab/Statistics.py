import math
from scipy.special import comb
from decimal import *

# test to see if results_2 are better than results_1 using sign test
# results_1/2 are lists of "+"/"-" corresponding to a correct/negative result respectively

class SignTest():
    def getSignificance(self,results_1,results_2):
       ties,plus,minus=0,0,0

       for i in range(0,len(results_1)):
           if results_1[i]==results_2[i]:
               ties+=1
               # "-" carries the error
           elif results_1[i]=="-": plus+=1
           elif results_2[i]=="-": minus+=1

       n = (2 * math.ceil(ties/2.0)) + plus + minus
       k = math.ceil(ties/2.0) + min(plus,minus)

       summation=Decimal(0.0)
       for i in range(0,int(k)+1):
           summation+=(Decimal(comb(n,i,exact=True)))

       # use two-tailed version of test
       summation *= 2

       summation *= (Decimal(0.5)**Decimal(n))
       return summation
