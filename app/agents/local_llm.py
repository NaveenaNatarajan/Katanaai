def analyze_title(title):
    if "men" in title.lower():
        return "Men's T-shirt"
    elif "women" in title.lower():
        return "Women's T-shirt"
    else:
        return "Unisex"
