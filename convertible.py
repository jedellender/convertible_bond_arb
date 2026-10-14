from dataclasses import dataclass
import numpy as np

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
    """