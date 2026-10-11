import numpy as np


def crr_params(sigma, r, q, T, N):
    # N = num steps

    dt = T / N  # defn time step
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp((r - q) * dt) - d) / (u - d)
    disc = np.exp(-r * dt) # discount factor

    if not 0 <= p <= 1:
        raise ValueError("Invalid parameters: p_up must be in [0, 1]")
    return u, d, p, disc, dt


def binomial_price(S, K, T, r, sigma, q, N):
    # calculate the price of a European option using CRR binomial model

    u, d, p_up, disc, dt = crr_params(S, sigma, r, q, T, N)
    p_down = 1-p_up

    # init asset prices at t=T.
    asset_prices = np.array([S * (u ** j) * (d ** (N - j)) for j in range(N + 1)])
    option_values = np.maximum(asset_prices - K, 0)

    # solve backwards for option price at t=0 
    for i in range(N - 1, -1, -1):
        option_values = disc * (p_up * option_values[1:i + 2] + p_down * option_values[0:i + 1])

    return option_values[0]


def stock_lattice(S, u, d, n):
    # generate lattice of stock prices 

    lattice = [ np.array([S * u**j * d**(i - j)
                          for j in range(i+1)
                          ])
                          for i in range(n+1)
                          ]
    return lattice

