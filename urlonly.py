import streamlit as st
import pandas as pd

def validate_data(data):
    # URL
    if not all(isinstance(item, str) for item in data['URL']):
        return "URL column should contain only strings."
    
    # Clicks
    if not all(isinstance(item, (int, float)) for item in data['Clicks']):
        return "Clicks column should contain only integers or floats."
    
    # Impressions
    if not all(isinstance(item, (int, float)) for item in data['Impressions']):
        return "Impressions column should contain only integers or floats."
    
    # CTR
    if not all(isinstance(item, (int, float)) for item in data['CTR']):
        return "CTR column should contain only integers or floats."
    
    # Position
    if not all(isinstance(item, (int, float)) for item in data['Position']):
        return "Position column should contain only integers or floats."

    return "Data is valid!"

def main():
    st.title("CSV Data Upload and Display")

    # Upload CSV
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            
            validation_message = validate_data(data)
            if validation_message == "Data is valid!":
                st.success(validation_message)
                
                # Slider in the sidebar for filtering by number of clicks
                min_clicks = int(data['Clicks'].min())
                max_clicks = int(data['Clicks'].max())
                
                clicks_range = st.sidebar.slider(
                    "Filter by number of clicks:",
                    min_clicks,
                    max_clicks,
                    (min_clicks, max_clicks)
                )
                
                filtered_data = data[(data['Clicks'] >= clicks_range[0]) & (data['Clicks'] <= clicks_range[1])]
                
                for index, row in filtered_data.iterrows():
                    st.text(f"URL: {row['URL']} | Clicks: {row['Clicks']}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
