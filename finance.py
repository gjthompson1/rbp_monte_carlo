from __future__ import division
import numpy as np
import pandas as pd
import math
from datetime import datetime
from calendar import monthrange
import scipy.optimize

def NPV(i, C):
    C = np.array(C)
    N = len(C)
    ans = np.sum(np.multiply(C[range(0, N)], np.power(1 / (1 + i), [range(0, N)])))
    return ans

def IRR(C):
    C = np.array(C)
    return scipy.optimize.brentq(NPV, -0.1, 1.0, args=C) * 12 * 100

def cum_int(P, rate, t, n):
    r = 1 + (rate / 12)
    ans = (P / (r ** n - 1)) * (t * (r ** n) * (r - 1) - ((r ** t) - 1))
    return ans

def rate_amortized(P, A, n):
    def rate_amortized_intermediate(rate, P, A, n):
        if round(rate,10) == 0:
            ans = P / n - A
        else:
            r = 1 + (rate / 100 / 12)
            ans = ((r ** n * (r - 1) * P) / (r**n - 1)) - A
        return ans
    return scipy.optimize.brentq(rate_amortized_intermediate, -100, 100, args=(P, A, n))/100

def payment_amortized(P, rate, n):
    if rate == 0:
        ans = P / n
    else:
        r = 1 + (rate / 100 / 12)
        ans = (r ** n * (r - 1) * P) / (r**n - 1)
    return (ans)

def risk_adj_rate(P,n,PD,LGD,RAR):
    def _risk_adj_func(i,P,n,PD,LGD,RAR):
        cashflow_risk_free = np.array([-P]+[payment_amortized(P,i,n)]*n)
        cashflow_true = np.array([-P]+[payment_amortized(P,RAR,n)]*n)
        ans=(1-PD)*(np.sum(cashflow_risk_free))-P*PD*LGD-np.sum(cashflow_true)
        return ans
    return scipy.optimize.brentq(_risk_adj_func, -100, 100, args=(P,n,PD,LGD,RAR))
