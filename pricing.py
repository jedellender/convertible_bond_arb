import numpy as np
from scipy.stats import norm

def bs_d1_d2(S, K, T, r, sigma, q):
    # q is continuous dividend, annulised decimal
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def bs_call(S, K, T, r, sigma, q):
    # Calculate the Black-Scholes price of a European call.

    d1, d2 = bs_d1_d2(S, K, T, r, sigma, q)

    call_price = S * np.exp(-q*T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    return call_price


