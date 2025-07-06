def decide(price_diff: float, reviews: int) -> str:
    """
    Decide marketing action based on price increase and number of reviews.
    """
    if reviews < 10:
        return "Needs Promotion"
    elif price_diff > 10:
        return "Premium Listing"
    return "Standard"
