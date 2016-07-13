import math
import numpy as np

def cnd(d):
    A1 = 0.31938153
    A2 = -0.356563782
    A3 = 1.781477937
    A4 = -1.821255978
    A5 = 1.330274429
    RSQRT2PI = 0.39894228040143267793994605993438
    K = 1.0 / (1.0 + 0.2316419 * np.abs(d))
    ret_val = (RSQRT2PI * np.exp(-0.5 * d * d) *
               (K * (A1 + K * (A2 + K * (A3 + K * (A4 + K * A5))))))
    return np.where(d > 0, 1.0 - ret_val, ret_val)

def blackscholes(callputflag, S, X, T, r, v):
    try:
        if T == 0:
            T = 0.0001;

        d1 = (math.log(S / X) + (r + v * v / 2) * T) / (v * math.sqrt(T))
        d2 = d1 - v * math.sqrt(T)

        if callputflag == 'C' or callputflag == 'c':
            bsPrice = S * cnd(d1) - X * math.exp(-r * T) * cnd(d2)
        else:
            bsPrice = X * math.exp(-r * T) * cnd(-d2) - S * cnd(-d1)
        return bsPrice
    except:
        #display( sprintf(' blackScholes error %s %f $f ', callPutFlag, S, X  ));
        return 0.0
