import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def bs_d1_d2(S, K, T, r, sigma, q):
    # q is continuous dividend, annulised decimal
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def call_px(S, K, T, r, sigma, q):
    # Calculate the Black-Scholes price of a European call.

    d1, d2 = bs_d1_d2(S, K, T, r, sigma, q)

    call_price = S * np.exp(-q*T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    return call_price


def bs_greeks(S, K, T, r, sigma, q):
    # calculate greeks assuming european call w/ cts. dividend

    d1, d2 = bs_d1_d2(S, K, T, r, sigma, q)

    delta = np.exp(-q *T) * norm.cdf(d1)
    gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = 1/365 * (-S * sigma * np.exp(-q * T) * norm.pdf(d1) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2) + q * S * np.exp(-q * T) * norm.cdf(d1)) # (daily) actual 365 convention
    vega = 1/100 * S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1) # per 1%pt change in vol
    rho = 1/100 * K * T * np.exp(-r * T) * norm.cdf(d2) # per 1%pt change in rate

    return delta, gamma, theta, vega, rho


def implied_vol(S, K, T, r, market_price, q=0.0, 
                low=1e-8, high=5.0):
    def f(sigma):
        return call_px(S, K, T, r, sigma, q) - market_price

    if f(low) * f(high) >0: # check interval contains zero (root)
        raise ValueError("No sign change: adjust the bracket for sigma.")

    return brentq(f, low, high, maxiter=1000)

