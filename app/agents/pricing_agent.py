def recommend_price(price: float, rating: float, reviews: int) -> float:
    """
    Recommend new price based on popularity metrics.
    - Increase price for highly rated/popular items.
    - Decrease price for poorly rated items.
    """
    if rating >= 4.5 and reviews >= 50:
        return round(price * 1.1, 2)
    elif rating < 3:
        return round(price * 0.9, 2)
    return round(price, 2)
