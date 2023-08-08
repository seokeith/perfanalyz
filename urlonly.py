import streamlit as st
import pandas as pd

def validate_data(data):
    if not all(isinstance(item, str) for item in data['URL']):
        return "URL column should contain only strings."
    
    if not all(isinstance(item, (int, float)) for item in data['Clicks']):
        return "Clicks column should contain only integers or floats."
    
    if not all(isinstance(item, (int, float)) for item in data['Impressions']):
        return "Impressions column should contain only integers or floats."
    
    if not all(isinstance(item, (int, float)) for item in data['CTR']):
        return "CTR column should contain only integers or floats."
    
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
                
                # URL dropdown filter in the sidebar
                selected_url = st.sidebar.selectbox(
                    'Select a URL:',
                    options=['All URLs'] + data['URL'].unique().tolist(),
                    format_func=lambda x: x if x != 'All URLs' else 'All URLs'
                )

                # If a specific URL is selected, filter the data by the selected URL
                if selected_url != 'All URLs':
                    data = data[data['URL'] == selected_url]
                
                # Slider in the sidebar for filtering by number of clicks
                min_clicks = int(data['Clicks'].min())
                max_clicks = int(data['Clicks'].max())

                if min_clicks != max_clicks:
                    clicks_range = st.sidebar.slider(
                        "Filter by number of clicks:",
                        min_clicks,
                        max_clicks,
                        (min_clicks, max_clicks)
                    )
                else:
                    clicks_range = (min_clicks, max_clicks)
                    st.sidebar.text(f"Only one value for clicks: {min_clicks}")

                # Calculate the average clicks
                avg_clicks = data['Clicks'].mean()
                st.sidebar.text(f"Average Clicks: {avg_clicks:.2f}")

                # Button to show URLs with lower than average clicks
                if st.sidebar.button("Show URLs with less than average clicks"):
                    lower_than_avg = data[data['Clicks'] < avg_clicks]
                    sorted_data = lower_than_avg.sort_values(by='Clicks', ascending=True)

                    for index, row in sorted_data.iterrows():
                        st.write(row['URL'], "-", row['Clicks'], "clicks")
                else:
                    filtered_data = data[(data['Clicks'] >= clicks_range[
