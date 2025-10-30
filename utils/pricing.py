def compute_resale_value(price, channel, condition):
    """Compute resale value based on condition and resale channel."""
    base = price
    recovery_rate = {
        "FedEx Thrift": 0.6,
        "Local Reseller": 0.7,
        "FedEx Global Return": 0.8
    }.get(channel, 0.65)
    condition_discount = {
        "New": 1.0,
        "Open-box": 0.85,
        "Used": 0.7,
        "Defective": 0.4
    }.get(condition, 0.7)
    return round(base * recovery_rate * condition_discount, 2)


def compute_merchant_payout(resale_value, return_fee):
    """Merchant’s final payout after return cost."""
    payout = resale_value - 0.25 * return_fee
    return round(payout, 2)
