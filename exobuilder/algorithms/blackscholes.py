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
    if d > 0:
        return 1.0 - ret_val
    else:
        return ret_val

def blackscholes(callputflag, ulprice, strike, toexpiry, riskfreerate, iv):
    try:
        if toexpiry <= 0:
            # Calculate payoff at expiration
            if callputflag == 'C' or callputflag == 'c':
                return max(0.0, ulprice - strike)
            else:
                return max(0.0, strike - ulprice)

        d1 = (math.log(ulprice / strike) + (riskfreerate + iv * iv / 2) * toexpiry) / (iv * math.sqrt(toexpiry))
        d2 = d1 - iv * math.sqrt(toexpiry)

        if callputflag == 'C' or callputflag == 'c':
            bsPrice = ulprice * cnd(d1) - strike * math.exp(-riskfreerate * toexpiry) * cnd(d2)
        else:
            bsPrice = strike * math.exp(-riskfreerate * toexpiry) * cnd(-d2) - ulprice * cnd(-d1)
        return bsPrice
    except:
        return 0.0

def blackscholes_greeks(callputflag, ulprice, strike, toexpiry, riskfreerate, iv):
    try:
        if toexpiry <= 0:
            # Calculate greeks at expiration
            if callputflag == 'C' or callputflag == 'c':
                delta = 1.0 if ulprice > strike else 0.0
            else:
                delta = -1.0 if ulprice < strike else 0.0
            return (delta, )

        d1 = (math.log(ulprice / strike) + (riskfreerate + iv * iv / 2) * toexpiry) / (iv * math.sqrt(toexpiry))
        d2 = d1 - iv * math.sqrt(toexpiry)
        if callputflag == 'C' or callputflag == 'c':
            # Call greeks
            call_delta = cnd(d1)
            return (call_delta, )
        else:
            # put greeks
            put_delta = -cnd(-d1)
            return (put_delta, )
    except:
        return (0.0,)

def blackscholes_gamma(callputflag, ulprice, strike, toexpiry, riskfreerate, iv):
    d1 = (math.log(ulprice / strike) + (riskfreerate + iv * iv / 2) * toexpiry) / (iv * math.sqrt(toexpiry))
    nd = math.exp(-d1 * d1 / 2) / 2.5066282746310002

    return nd / (ulprice * iv * math.sqrt(toexpiry))
