import streamlit as st
import pandas as pd
from utils.data_processing import process_file, convert_to_numeric
from utils.predictions import generate_forecast
from utils.display import display_results

# Streamlit UI
st.title("Carbon Neutrality Prediction")
st.write("Upload a CSV file and configure parameters for forecasting energy use and carbon emissions.")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Input parameters
low_emission_threshold = st.number_input("Low Emission Threshold (kg CO2)", value=10000000, step=100000)
forecast_years = st.number_input("Forecast Years", value=16, step=1)

st.write("### Fossil Fuel Reduction Rates (Decimal Percentage)")
coal_red = st.slider("Coal Reduction Rate", 0.0, 1.0, 0.15)
natural_red = st.slider("Natural Gas Reduction Rate", 0.0, 1.0, 0.15)
furnace_red = st.slider("Furnace Oil Reduction Rate", 0.0, 1.0, 0.15)
grid_red = st.slider("Grid Electricity Reduction Rate", 0.0, 1.0, 0.15)
hsd_red = st.slider("HSD Reduction Rate", 0.0, 1.0, 0.15)

fossil_reduction_rate = [coal_red, natural_red, furnace_red, grid_red, hsd_red]

# Add a button to start predictions
if st.button("Make Predictions"):
    if uploaded_file:
        # Process uploaded data
        data = process_file(uploaded_file)
        if data is not None:
            # Generate forecasts
            forecast_df, carbon_neutral_month, low_emission_month = generate_forecast(
                data, low_emission_threshold, forecast_years, fossil_reduction_rate
            )

            # Display results
            display_results(forecast_df, carbon_neutral_month, low_emission_month)
        else:
            st.error("Error processing the uploaded file.")
    else:
        st.error("Please upload a CSV file.")
