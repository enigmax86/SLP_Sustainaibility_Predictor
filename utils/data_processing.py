import pandas as pd

def convert_to_numeric(df, columns):
    """Convert specified columns to numeric format."""
    for column in columns:
        df[column] = pd.to_numeric(df[column].astype(str).str.replace(',', ''), errors='coerce')
    return df

def process_file(uploaded_file):
    """Process the uploaded CSV file and return a cleaned DataFrame."""
    try:
        data = pd.read_csv(uploaded_file)
        columns_to_convert = ['Coal', 'Natural Gas', 'Furnace Oil', 'Grid Electricity',
                              'HSD', 'Solar Energy', 'Wind Energy', 'Biomass', 'Hybrid Energy', 'Total Energy (GJ)']
        data = convert_to_numeric(data, columns_to_convert)
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
        data = data.drop(columns=['Steam Purchased', 'LPG'], errors='ignore')
        data.set_index('Date', inplace=True)
        return data
    except Exception as e:
        print(f"Error processing file: {e}")
        return None
