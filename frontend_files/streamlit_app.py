import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="SuperKart Sales Predictor", layout="wide")
st.title("SuperKart Sales Prediction")
st.markdown("Predict the sales revenue for products across SuperKart outlets.")

# Backend API URL
BACKEND_URL = "http://backend:7860"

# --- Sidebar for navigation ---
option = st.sidebar.selectbox("Choose Prediction Mode", ["Online (Single)", "Batch"])

if option == "Online (Single)":
    st.header("Online Prediction")
    st.markdown("Enter product and store details to predict sales revenue.")

    col1, col2 = st.columns(2)

    with col1:
        product_weight = st.number_input("Product Weight", min_value=0.0, max_value=30.0, value=12.66)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
        product_mrp = st.number_input("Product MRP", min_value=0.0, max_value=300.0, value=117.08)
        product_id_char = st.selectbox("Product ID Category", ["FD", "DR", "NC"])

    with col2:
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        store_location = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
        store_age = st.number_input("Store Age (Years)", min_value=0, max_value=50, value=16)
        product_type_cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

    if st.button("Predict Sales"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar,
            "Product_Allocated_Area": product_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": store_age,
            "Product_Type_Category": product_type_cat,
        }
        try:
            response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
            result = response.json()
            st.success(f"Predicted Sales Revenue: **${result['prediction']:,.2f}**")
        except Exception as e:
            st.error(f"Error: {e}")

elif option == "Batch":
    st.header("Batch Prediction")
    st.markdown("Upload a CSV file with product and store features to get batch predictions.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.dataframe(input_df.head())

        if st.button("Get Batch Predictions"):
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file.getvalue()})
                predictions = response.json()
                input_df["Predicted_Sales"] = [predictions[str(i)] for i in range(len(input_df))]
                st.write("Predictions:")
                st.dataframe(input_df)
            except Exception as e:
                st.error(f"Error: {e}")
