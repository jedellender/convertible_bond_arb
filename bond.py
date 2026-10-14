import numpy as np

def coupon_schedule(face, coupon_rate, T, freq=2):
    # coupon schedule
    # face: face value of the bond
    # coupon_rate: annual coupon rate (as decimal)
    # T: time to maturity in years
    # freq: coupon frequency

    num_payments = int(T * freq)

    coupon_payment = face * coupon_rate / freq

    schedule = [coupon_payment] * num_payments

    schedule[-1] += face  # add face value to last payment

    return schedule

# to add year_fraction function for real bonds with differing conventions


def discount_factors(T, freq=2 ,discount_rate=0.05):
    # returns array of discount factors per coupon

    num_payments = T * freq
    times = np.arange(1, num_payments + 1) / freq
    #t: times
    #r: rate
    times = np.asarray(times)
    return np.exp(-discount_rate * times)

