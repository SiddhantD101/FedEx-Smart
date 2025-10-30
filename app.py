import streamlit as st
import pandas as pd
import numpy as np
import time

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="FedEx Global Returns Estimator",
    layout="wide",
    page_icon="📦",
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/sample_data.csv")

products_df = load_data()

# Ensure proper column naming
if "Product ID" in products_df.columns:
    products_df.rename(columns={"Product ID": "product_id"}, inplace=True)

products_df["product_id"] = products_df["product_id"].astype(int)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #F8F8F8;
    }
    .title {
        text-align: center;
        color: #4D148C;  /* FedEx Purple */
        font-size: 2.4em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #FF6600;  /* FedEx Orange */
        font-size: 1.1em;
        margin-bottom: 35px;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 1px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:first-child {
        background-color: #FF6600;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #E85B00;
        transform: scale(1.02);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='title'>FedEx Global Returns Estimator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Estimate return logistics, costs, and resale options for merchants worldwide.</div>", unsafe_allow_html=True)

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("🧾 Merchant Input")

product_id = st.sidebar.number_input(
    "Enter Product ID",
    min_value=int(products_df["product_id"].min()),
    max_value=int(products_df["product_id"].max()),
    step=1,
)

distance = st.sidebar.slider("Select return distance (km)", 10, 5000, 250)

platform = st.sidebar.selectbox("Select selling platform", ["FedEx", "FedEx Thrift", "Other"])

estimate_btn = st.sidebar.button("Estimate Return Fee 🚀")

# -----------------------------
# Main Section
# -----------------------------
if estimate_btn:
    # Fetch product details
    product = products_df.loc[products_df["product_id"] == int(product_id)]

    if product.empty:
        st.error("❌ Product ID not found in dataset.")
    else:
        product_details = product.iloc[0]

        # --- Interactive Progress Animation ---
        with st.spinner("Calculating estimated return fee..."):
            progress_bar = st.progress(0)
            steps = 50
            for i in range(steps):
                time.sleep(0.02)  # simulate calculation
                progress_bar.progress(int((i + 1) / steps * 100))
            progress_bar.empty()
        st.success("✅ Estimation complete!")

        # --- Fee Calculation ---
        base_fee = 50
        weight_factor = np.random.uniform(0.5, 1.5)
        distance_factor = distance * 0.1
        estimated_fee = round(base_fee + distance_factor * weight_factor, 2)

        # --- Display Result Summary ---
        st.subheader("📊 Estimated Return Summary")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="📦 Product ID", value=int(product_id))
        with col2:
            st.metric(label="🌍 Return Distance (km)", value=distance)
        with col3:
            st.metric(label="💰 Estimated Return Fee ($)", value=estimated_fee)

        st.markdown("---")

        # --- Product Info Display ---
        st.subheader("🛍️ Product Details")
        colA, colB = st.columns([2, 1])

        with colA:
            st.dataframe(product, use_container_width=True)
        with colB:
            st.markdown(
                f"""
                <div class='metric-card'>
                <h4 style='color:#4D148C;'>Quick Summary</h4>
                <ul>
                    <li><b>Category:</b> {product_details.get('category', 'N/A')}</li>
                    <li><b>Weight:</b> {product_details.get('weight', 'N/A')} kg</li>
                    <li><b>Price:</b> ${product_details.get('price', 'N/A')}</li>
                    <li><b>Stock:</b> {product_details.get('stock', 'N/A')}</li>
                </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # --- Decision Recommendation ---
        st.markdown("---")
        st.subheader("🧭 Recommended Action")

        if estimated_fee > product_details.get("price", 100):
            st.warning("⚠️ Return not feasible — suggest resale or discount.")
        else:
            st.success("✅ Proceed with standard global return logistics.")

        # --- Redirect Option ---
        # --- Redirect Option ---
        if platform == "FedEx Thrift":
            st.markdown("---")
            st.markdown("<h3 style='color:#FF6600;'>♻️ Resell on FedEx Thrift</h3>", unsafe_allow_html=True)
            thrift_url = "http://localhost:8502"  # Target thrift app
            st.link_button("Go to FedEx Thrift Marketplace 🛍️", thrift_url)

        else:
            st.info(f"Processing return via **{platform}** platform.")

else:
    st.markdown("👈 Enter product details on the left to begin estimation.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 FedEx Labs – Internal Prototype Demo</p>",
    unsafe_allow_html=True,
)
