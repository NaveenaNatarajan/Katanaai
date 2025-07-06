import streamlit as st
from myagents import run_pipeline
from config import DATA_PATH, IMAGE_FOLDER
import pandas as pd
import os

# Load data
df = pd.read_csv(DATA_PATH)
total_items = len(df)

# UI Setup
st.set_page_config(page_title="T-shirt Analyzer", layout="centered")
st.title("👕 T-shirt Analysis - Agentic AI Pipeline")

index = st.slider("Select T-shirt Image Index", 1, total_items, 1)

if st.button("🔍 Analyze T-shirt"):
    with st.spinner("Running AI Agents..."):
        result = run_pipeline(image_index=index)

    st.subheader("🖼️ Product Image")
    st.image(os.path.join(IMAGE_FOLDER, f"tshirt_{index}.jpg"), caption="T-shirt Image", use_container_width=True)

    st.subheader("📋 Product Summary")
    st.markdown(f"**Title:** {result['title']}")
    st.markdown(f"**Image Description:** {result['description']}")
    st.markdown(f"**Category:** {result['category']}")
    st.markdown(f"**Keywords:** {result['keywords']}")
    st.metric("💰 Recommended Price", f"₹{result['new_price']:.2f}")
    st.success(result["action"])

    st.subheader("💬 Full Agent Conversation Log")
    for entry in result["full_chat"]:
        st.markdown(entry)

