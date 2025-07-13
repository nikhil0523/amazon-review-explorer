#!/usr/bin/env python
# coding: utf-8

# In[14]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from difflib import get_close_matches

# === Helper function to normalize names ===
def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[|&()_,.:;'\-]", " ", text)  # remove special characters
    text = re.sub(r"\s+", " ", text).strip()     # collapse multiple spaces
    return text

# === Set Streamlit page config ===
st.set_page_config(page_title="Amazon Review Explorer", layout="wide")
st.title("📦 Amazon Reviews Topic & Sentiment Explorer")

# === Load data ===
@st.cache_data
def load_data():
    return pd.read_csv("Sent.csv")

df = load_data()

# === Sidebar filters ===
st.sidebar.header("🔍 Filter Options")
product = st.sidebar.selectbox("Select Product", options=["All"] + sorted(df['Name'].unique().tolist()))
topic = st.sidebar.selectbox("Select Topic", options=["All"] + sorted(df['Topic_Label'].unique().tolist()))
sentiment = st.sidebar.selectbox("Select Sentiment", options=["All", "Positive", "Neutral", "Negative"])

# === Filter data based on selections ===
filtered_df = df.copy()
if product != "All":
    filtered_df = filtered_df[filtered_df['Name'] == product]
if topic != "All":
    filtered_df = filtered_df[filtered_df['Topic_Label'] == topic]
if sentiment != "All":
    filtered_df = filtered_df[filtered_df['Sentiment_Label'] == sentiment]

st.markdown(f"### Showing {len(filtered_df)} filtered reviews")

# === Image and Product Stats ===
if product != "All":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Product Stats")
        st.write(f"**Total reviews:** {len(df[df['Name'] == product])}")
        st.write(f"**Available topics:** {filtered_df['Topic_Label'].nunique()}")
        st.write(f"**Sentiments:** {filtered_df['Sentiment_Label'].value_counts().to_dict()}")

    with col2:
        st.subheader("🖼️ Product Image")

        # --- Image directory ---
        image_dir = "Amaz1"
        product_normalized = normalize(product)

        # Load and normalize image filenames
        image_files = os.listdir(image_dir)
        image_basename_map = {
            normalize(os.path.splitext(f)[0]): f for f in image_files
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
        }

        # Fuzzy match against normalized names
        closest_match = get_close_matches(product_normalized, list(image_basename_map.keys()), n=1, cutoff=0.7)

        if closest_match:
            matched_filename = image_basename_map[closest_match[0]]
            matched_image = os.path.join(image_dir, matched_filename)
            st.image(matched_image, caption=product, use_container_width=True)
        else:
            st.warning("⚠️ No matching image found in folder.")

# === Topic Distribution ===
if not filtered_df.empty:
    st.subheader("📈 Topic Distribution")
    topic_counts = filtered_df['Topic_Label'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=topic_counts.index, y=topic_counts.values, ax=ax, palette='Blues_d')
    ax.set_ylabel("Number of Reviews")
    ax.set_xlabel("Topic")
    plt.xticks(rotation=30)
    st.pyplot(fig)

    # === Sentiment Distribution ===
    st.subheader("😊 Sentiment Distribution")
    sentiment_counts = filtered_df['Sentiment_Label'].value_counts()
    fig2, ax2 = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax2, palette='coolwarm')
    ax2.set_ylabel("Number of Reviews")
    ax2.set_xlabel("Sentiment")
    st.pyplot(fig2)

    # === Sample Reviews ===
    st.subheader("📝 Sample Reviews")
    for i, row in filtered_df.head(5).iterrows():
        st.markdown(f"**Topic:** {row['Topic_Label']} | **Sentiment:** {row['Sentiment_Label']}")
        st.write(row['Reviews'])
        st.markdown("---")
else:
    st.info("No reviews found for selected filters.")


# In[6]:





# In[ ]:





# In[ ]:





# In[ ]:




