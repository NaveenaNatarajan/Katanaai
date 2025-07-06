from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from app.agents.vision_agent import describe_image_with_blip
from app.agents.product_analyst import analyze_title_llm, extract_keywords
from app.agents.pricing_agent import recommend_price
from app.agents.decision_agent import decide
from config import DATA_PATH, IMAGE_FOLDER
import pandas as pd
import os

# === Agents ===

common_llm_config = {
    "config_list": [{
        "model": "gemini-2.5-flash",     # Gemini model
        "api_key": os.getenv("GEMINI_API_KEY"),
        "base_url": "https://generativelanguage.googleapis.com/v1beta",  # required for Gemini
        "api_type": "google"
    }]
}

vision_agent = AssistantAgent(
    name="VisionAgent",
    system_message="Describe the T-shirt image.",
    llm_config=common_llm_config,
    function_map={"describe_image": describe_image_with_blip}
)

product_analyst = AssistantAgent(
    name="ProductAnalyst",
    system_message="Extract category and keywords from product description.",
    llm_config=common_llm_config,
    function_map={
        "analyze_title": analyze_title_llm,
        "extract_keywords": extract_keywords
    }
)

pricing_agent = AssistantAgent(
    name="PricingAgent",
    system_message="Recommend a new price based on rating and reviews.",
    llm_config=common_llm_config,
    function_map={"recommend_price": recommend_price}
)

decision_agent = AssistantAgent(
    name="DecisionAgent",
    system_message="Decide on marketing action based on price difference and reviews.",
    llm_config=common_llm_config,
    function_map={"decide_action": decide}
)

user_proxy = UserProxyAgent(
    name="User",
    code_execution_config=False,
    human_input_mode="NEVER"
)

# === Run the Agentic Pipeline ===

def run_pipeline(image_index: int):
    logs = []

    df = pd.read_csv(DATA_PATH)
    df["price"] = df["price"].replace('[₹,]', '', regex=True).astype(float)
    df["reviews"] = df["reviews"].replace(',', '', regex=True).astype(int)

    row = df.iloc[image_index - 1]
    image_path = os.path.join(IMAGE_FOLDER, f"tshirt_{image_index}.jpg")

    title = row["title"]
    original_price = row["price"]
    rating = row["rating"]
    reviews = row["reviews"]

    # Construct prompt
    prompt = (
        f"You are an AI team analyzing a T-shirt product.\n"
        f"Image Path: {image_path}\n"
        f"Title: {title}\n"
        f"Price: ₹{original_price}, Rating: {rating}, Reviews: {reviews}\n"
        f"Steps:\n"
        f"1. VisionAgent describes the image.\n"
        f"2. ProductAnalyst extracts category and keywords.\n"
        f"3. PricingAgent recommends a new price.\n"
        f"4. DecisionAgent suggests a marketing action.\n"
    )
    logs.append(f"🟡 Prompt sent to agents:\n{prompt}")

    group_chat = GroupChat(
        agents=[user_proxy, vision_agent, product_analyst, pricing_agent, decision_agent],
        messages=[],
        max_round=8
    )
    manager = GroupChatManager(groupchat=group_chat, llm_config=common_llm_config)
 # ... existing code

    user_proxy.initiate_chat(recipient=manager, message=prompt)

    # Capture full conversation
    full_chat_log = []
    for msg in group_chat.messages:
        role = msg["name"]
        content = msg["content"]
        full_chat_log.append(f"**{role}**:\n{content}\n---")

    # Optional tools
    description = describe_image_with_blip(image_path)
    category = analyze_title_llm(description)
    keywords = extract_keywords(description)
    new_price = recommend_price(original_price, rating, reviews)
    action = decide(new_price - original_price, reviews)

    return {
        "title": title,
        "description": description,
        "category": category,
        "keywords": keywords,
        "new_price": new_price,
        "action": action,
        "full_chat": full_chat_log
    }



# === Run Example ===
if __name__ == "__main__":
    run_pipeline(image_index=8)  # Change this index to test others
