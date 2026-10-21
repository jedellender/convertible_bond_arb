from dataclasses import dataclass
import numpy as np
from trees import crr_params, stock_lattice

def conversion_ratio(face, conversion_price):
    """Number of shares received on conversion."""
    return face / conversion_price


def parity(S, conversion_ratio):
    """Value of the conversion shares."""
    return S * conversion_ratio


def conversion_premium(price, parity_value):
    """Convertible price divided by parity minus one."""
    return price / parity_value - 1


def investment_premium(price, floor_value):
    """Convertible price divided by bond floor minus one."""
    return price / floor_value - 1


@dataclass
class TFLatticeResult:
    price: float
    stock: list[np.ndarray]
    equity: list[np.ndarray]
    cash: list[np.ndarray]

# Starting function with _, so it is private, non-importable
def _validate_tf_inputs(
    S,
    face,
    coupon_rate,
    conversion_price,
    T,
    r,
    spread,
    sigma,
    q,
    n,
    freq,
):
    values = {
        "S": S,
        "face": face,
        "coupon_rate": coupon_rate,
        "conversion_price": conversion_price,
        "T": T,
        "r": r,
        "spread": spread,
        "sigma": sigma,
        "q": q,
        "n": n,
        "freq": freq,
    }
    for name, value in values.items():
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")

    positive = {
        "S": S,
        "face": face,
        "conversion_price": conversion_price,
        "T": T,
        "sigma": sigma,
    }
    for name, value in positive.items():
        if value <= 0:
            raise ValueError(f"{name} must be positive")

    if coupon_rate < 0:
        raise ValueError("coupon_rate must be non-negative")
    if spread < 0:
        raise ValueError("spread must be non-negative")
    if n < 1 or int(n) != n:
        raise ValueError("n must be a positive integer")
    if freq < 1 or int(freq) != freq:
        raise ValueError("freq must be a positive integer")

    n = int(n)
    freq = int(freq)
    coupon_periods = T * freq
    if not np.isclose(coupon_periods, round(coupon_periods)):
        raise ValueError("T * freq must be a whole number of coupon periods")

    coupon_periods = int(round(coupon_periods))
    if n % coupon_periods:
        raise ValueError("n must be divisible by the number of coupon periods")
    return n, freq, coupon_periods


def tf_price(
    S,
    face,
    coupon_rate,
    conversion_price,
    T,
    r,
    spread,
    sigma,
    q=0.0,
    n=200,
    freq=2,
):
    """
    Price a non-callable, non-puttable convertible using
    the Tsiveriotis-Fernandes lattice.

    The equity component is discounted at ``r`` and the cash component at
    ``r + spread``. Coupons are paid at the requested frequency. The returned
    lattices are ordered by time, with the stock lattice at index ``i``
    containing ``i + 1`` nodes.
    """
    n, freq, coupon_periods = _validate_tf_inputs(
        S,
        face,
        coupon_rate,
        conversion_price,
        T,
        r,
        spread,
        sigma,
        q,
        n,
        freq,
    )
    cr = conversion_ratio(face, conversion_price)
    up, down, p_up, equity_discount, dt = crr_params(sigma, r, q, T, n)
    p_down = 1 - p_up
    cash_discount = np.exp(-(r + spread) * dt)
    stock = stock_lattice(S, up, down, n)
    equity = [np.empty(i + 1, dtype=float) for i in range(n + 1)]
    cash = [np.empty(i + 1, dtype=float) for i in range(n + 1)]

    final_coupon = face * coupon_rate / freq
    terminal_parity = cr * stock[-1]
    terminal_redemption = face + final_coupon
    converts = terminal_parity >= terminal_redemption
    equity[-1][:] = np.where(converts, terminal_parity, 0.0)
    cash[-1][:] = np.where(converts, 0.0, terminal_redemption)

    steps_per_coupon = n // coupon_periods
    for i in range(n - 1, -1, -1):
        equity_cont = equity_discount * (
            p_up * equity[i + 1][1:] + p_down * equity[i + 1][:-1]
        )
        cash_cont = cash_discount * (
            p_up * cash[i + 1][1:] + p_down * cash[i + 1][:-1]
        )
        if i > 0 and i % steps_per_coupon == 0:
            cash_cont += final_coupon

        continuation = equity_cont + cash_cont
        conversion_value = cr * stock[i]
        converts = conversion_value > continuation
        equity[i][:] = np.where(converts, conversion_value, equity_cont)
        cash[i][:] = np.where(converts, 0.0, cash_cont)

    return TFLatticeResult(
        price=float(equity[0][0] + cash[0][0]),
        stock=stock,
        equity=equity,
        cash=cash,
    )
