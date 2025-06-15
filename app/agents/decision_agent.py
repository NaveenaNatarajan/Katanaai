def decide(price_diff, reviews):
    if reviews < 10:
        return "Needs Promotion"
    elif price_diff > 10:
        return "Premium Listing"
    return "Standard"
