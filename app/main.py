from config import DATA_PATH, IMAGE_FOLDER, OUTPUT_FILE
from agents.local_llm import analyze_title
from agents.vision_agent import describe_image_with_blip
from agents.pricing_agent import get_new_price
from agents.decision_agent import decide
import pandas as pd
import os

df = pd.read_csv(DATA_PATH)
results = []

# Clean price and reviews columns in case they contain symbols or commas
df["price"] = df["price"].replace('[₹,]', '', regex=True).astype(float)
df["reviews"] = df["reviews"].replace(',', '', regex=True).astype(int)

for idx, row in df.iterrows():
    img_path = os.path.join(IMAGE_FOLDER, f"tshirt_{idx+1}.jpg")
    title_tag = analyze_title(row["title"])
    description = describe_image_with_blip(img_path)
    price = float(row["price"])
    reviews = int(row["reviews"])
    new_price = get_new_price(price, row["rating"], reviews)
    action = decide(new_price - price, reviews)

    results.append({
        "title": row["title"],
        "title_tag": title_tag,
        "image_description": description,
        "original_price": price,
        "new_price": new_price,
        "action": action
    })

pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
print("Analysis complete! Results saved to", OUTPUT_FILE)
