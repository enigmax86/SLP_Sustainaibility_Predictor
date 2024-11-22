import streamlit as st
import pandas as pd 

def display_results(forecast_df, carbon_neutral_month, low_emission_month):
    """Display results in the Streamlit app."""
    if pd.notna(carbon_neutral_month):
        st.success(f"Projected carbon neutrality by: {carbon_neutral_month.strftime('%B %Y')}")
    else:
        st.warning("Carbon neutrality not achieved within the forecasted range.")

    if pd.notna(low_emission_month):
        st.info(f"Projected low emission threshold (<1,00,00,000 kg CO2) by: {low_emission_month.strftime('%B %Y')}")
    else:
        st.warning("Low emission threshold not achieved within the forecasted range.")

    st.write("### Predictions Table")
    st.dataframe(forecast_df)

    st.write("### Download Predictions")
    csv = forecast_df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="Download Predictions as CSV",
        data=csv,
        file_name='Carbon_Neutrality_Projection.csv',
        mime='text/csv',
    )
