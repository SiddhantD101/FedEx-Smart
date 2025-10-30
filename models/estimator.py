import pandas as pd
import numpy as np

def fetch_product_details(product_id):
    """Fetch product info from CSV based on product_id."""
    df = pd.read_csv("data/sample_data.csv")
    try:
        product = df[df["product_id"] == int(product_id)].iloc[0]
        return {
            "id": product["product_id"],
            "name": product["product_name"],
            "category": product["category"],
            "price": product["price"],
            "weight": product["weight"]
        }
    except (IndexError, ValueError):
        return None


def estimate_return_fee(price, weight, category, distance_km):
    """Estimate return shipping fee based on product, category, and distance."""
    base_rate = 0.05 * price
    weight_factor = weight * 100  # ₹100 per kg
    distance_factor = distance_km * 0.5  # ₹0.5 per km
    category_factor = {
        "Electronics": 1.2,
        "Clothing": 0.8,
        "Furniture": 1.5,
        "Accessories": 0.6,
        "Other": 1.0
    }.get(category, 1.0)
    fee = (base_rate + weight_factor + distance_factor) * category_factor
    return round(fee, 2)
