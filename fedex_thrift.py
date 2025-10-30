import streamlit as st
import pandas as pd
import os

# CSV to store listed products
DATA_PATH = "data/thrift_listings.csv"
os.makedirs("data", exist_ok=True)

# Create CSV if not exist
if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(columns=["Product Name", "Category", "Condition", "Price"])
    df.to_csv(DATA_PATH, index=False)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FedEx Thrift", page_icon="🛍️", layout="wide")

st.title("🛍️ FedEx Thrift Marketplace")
st.markdown("Sell returned items or buy pre-loved ones with ease and transparency.")

st.divider()

# ---------------- LISTINGS ----------------
st.subheader("🧾 Available Listings")

df = pd.read_csv(DATA_PATH)
if df.empty:
    st.info("No products listed yet. Be the first to add yours below 👇")
else:
    for i, row in df.iterrows():
        with st.container():
            st.markdown(f"""
            **{row['Product Name']}**  
            _Category:_ {row['Category']} | _Condition:_ {row['Condition']}  
            💰 **Price:** ${row['Price']}
            """)
            st.divider()

# ---------------- ADD PRODUCT FORM ----------------
st.subheader("➕ Add Your Product for Resale")

with st.form("add_product_form"):
    name = st.text_input("Product Name")
    category = st.selectbox("Category", ["Electronics", "Clothing", "Furniture", "Accessories", "Other"])
    condition = st.selectbox("Condition", ["New", "Like New", "Used", "Refurbished"])
    price = st.number_input("Price ($)", min_value=1.0, step=1.0)
    submitted = st.form_submit_button("Add Listing")

if submitted:
    if name:
        new_row = pd.DataFrame([[name, category, condition, price]], 
                               columns=["Product Name", "Category", "Condition", "Price"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success(f"✅ '{name}' has been listed successfully!")
        st.experimental_rerun()
    else:
        st.error("Please enter a valid product name.")
