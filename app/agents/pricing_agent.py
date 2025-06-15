def get_new_price(price, rating, reviews):
    if rating >= 4.5 and reviews >= 50:
        return round(price * 1.1, 2)
    elif rating < 3:
        return round(price * 0.9, 2)
    return price
