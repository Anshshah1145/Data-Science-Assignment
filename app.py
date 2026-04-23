import streamlit as st
import pickle
import pandas as pd

# -------------------------
# LOAD MODELS
# -------------------------
reg_model = pickle.load(open("reg_model.pkl", "rb"))
clf_model = pickle.load(open("clf_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="EverGreen Homes", layout="wide")

# -------------------------
# UI DESIGN
# -------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.stButton>button {
    background-color: #00c853;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏠 EverGreen Home Price Predictor")

# -------------------------
# USER INPUTS
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    area = st.number_input("Area (sq ft)", 500, 10000, 1000)

with col2:
    bedrooms = st.number_input("Bedrooms", 1, 10, 2)

with col3:
    bathrooms = st.number_input("Bathrooms", 1, 10, 2)

# Extract location names from columns
location_cols = [col for col in columns if col.startswith("Location_")]
locations = [col.replace("Location_", "") for col in location_cols]

location = st.selectbox("Location", locations)

model_type = st.selectbox("Select Model", ["Regression", "Classification"])

# -------------------------
# PREDICTION
# -------------------------
if st.button("Predict"):

    # Create empty input
    input_dict = {col: 0 for col in columns}

    # Fill numeric values (IMPORTANT: match column names exactly)
    if "Area" in input_dict:
        input_dict["Area"] = area

    if "No. of Bedrooms" in input_dict:
        input_dict["No. of Bedrooms"] = bedrooms

    if "BED" in input_dict:
        input_dict["BED"] = bedrooms

    # Location encoding
    loc_col = f"Location_{location}"
    if loc_col in input_dict:
        input_dict[loc_col] = 1

    # Convert to dataframe
    input_df = pd.DataFrame([input_dict])

    # -------------------------
    # MODEL PREDICTION
    # -------------------------
    if model_type == "Regression":
        pred = reg_model.predict(input_df)[0]
        pred = max(0, pred)  # prevent negative
        st.success(f"💰 Estimated Price: ₹ {pred:,.2f}")

    else:
        pred = clf_model.predict(input_df)[0]
        st.success(f"📊 Price Category: {pred}")