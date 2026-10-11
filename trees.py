import numpy as np


def crr_params(sigma, r, q, T, N):
    # N = num steps

    dt = T / N  # defn time step
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p_up = (np.exp((r - q) * dt) - d) / (u - d)
    p_down = 1 - p_up

    if not 0 <= p_up <= 1:
        raise ValueError("Invalid parameters: p_up must be in [0, 1]")

    return u, d, p_up, p_down


def binomial_price(S, K, T, r, sigma, q, N):
    # calculate the price of a European option using CRR binomial model

    u, d, p_up, p_down = crr_params(S, sigma, r, q, T, N)
    dt = T / N

    # init asset prices at maturity
    asset_prices = np.array([S * (u ** j) * (d ** (N - j)) for j in range(N + 1)])

    option_values = np.maximum(asset_prices - K, 0)

    # solve backwards for option price at t=0 
    for i in range(N - 1, -1, -1):
        option_values = np.exp(-r * dt) * (p_up * option_values[1:i + 2] + p_down * option_values[0:i + 1])

    return option_values[0]


