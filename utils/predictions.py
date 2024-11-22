import pandas as pd
from prophet import Prophet

def generate_forecast(data, low_emission_threshold, forecast_years, fossil_reduction_rate):
    """Generate forecast and calculate carbon neutrality and low-emission dates."""
    emission_factors = {
        'Coal': 94.6, 'Natural Gas': 56.1, 'Furnace Oil': 77.43273849,
        'HSD': 70.73425004, 'Solar Energy': 0, 'Wind Energy': 0,
        'Biomass': 0, 'Hybrid Energy': 0
    }
    grid_electricity_factors = {
        2023: 166.062775, 2024: 86.7709, 2025: 84.3808, 2026: 82.3108,
        # Add more years if needed...
    }

    # Prepare Prophet model
    prophet_data = data[['Total Energy (GJ)']].reset_index().rename(columns={'Date': 'ds', 'Total Energy (GJ)': 'y'})
    prophet_model = Prophet(yearly_seasonality=True)
    prophet_model.fit(prophet_data)

    carbon_neutral_month = None
    low_emission_month = None

    # Forecast loop
    while carbon_neutral_month is None or low_emission_month is None:
        future_dates = prophet_model.make_future_dataframe(periods=forecast_years * 12, freq='MS')
        future_dates = future_dates[future_dates['ds'] >= '2024-01']
        prophet_forecast = prophet_model.predict(future_dates)
        forecast_df = prophet_forecast[['ds', 'yhat']].rename(columns={'ds': 'Date', 'yhat': 'Total Energy (GJ)'}).set_index('Date')

        latest_percents = data.iloc[-1].drop('Total Energy (GJ)') / data.iloc[-1]['Total Energy (GJ)']

        for month, date in enumerate(forecast_df.index, start=1):
            fossil_fuel_sources = ['Coal', 'Natural Gas', 'Furnace Oil', 'Grid Electricity', 'HSD']
            renewable_sources = ['Solar Energy', 'Wind Energy', 'Biomass', 'Hybrid Energy']
            reduction_multiplier = [(1 - i) ** (month // 12) for i in fossil_reduction_rate]

            fossil_percentage = pd.Series([latest_percents[src] * mult for src, mult in zip(fossil_fuel_sources, reduction_multiplier)],
                                          index=fossil_fuel_sources)
            renewable_percentage_increase = (1 - fossil_percentage.sum()) / len(renewable_sources)

            forecast_df.loc[date, fossil_fuel_sources] = fossil_percentage.values
            forecast_df.loc[date, renewable_sources] = renewable_percentage_increase

        # Carbon footprint calculation
        forecast_df['Carbon Footprint (kg CO2)'] = 0
        for source, factor in emission_factors.items():
            factor = grid_electricity_factors.get(forecast_df.index[0].year, factor) if source == 'Grid Electricity' else factor
            forecast_df['Carbon Footprint (kg CO2)'] += forecast_df[source] * forecast_df['Total Energy (GJ)'] * factor

        # Determine carbon neutrality and low-emission threshold
        if carbon_neutral_month is None:
            carbon_neutral_month = forecast_df[forecast_df['Carbon Footprint (kg CO2)'] <= 0].index.min()
        if low_emission_month is None:
            low_emission_month = forecast_df[forecast_df['Carbon Footprint (kg CO2)'] <= low_emission_threshold].index.min()

        if carbon_neutral_month is None or low_emission_month is None:
            forecast_years += 5

    return forecast_df, carbon_neutral_month, low_emission_month
