import streamlit as st
import pandas as pd

def main():
    st.title('CSV Data Viewer')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        data = pd.read_csv(uploaded_file)

        # Validate the CSV format
        expected_columns = ["URL", "Clicks", "Impressions", "CTR", "Position"]
        if not all(col in data.columns for col in expected_columns):
            st.error('Invalid CSV file format. Please make sure the CSV has the required columns.')
            return

        # Filter controls
        st.sidebar.header('Filters')

        # Filter by URL
        unique_urls = data['URL'].unique().tolist()
        selected_url = st.sidebar.multiselect('URL', unique_urls, default=unique_urls)
        data = data[data['URL'].isin(selected_url)]

        # Filter by Clicks
        min_clicks, max_clicks = st.sidebar.slider('Clicks', int(data['Clicks'].min()), int(data['Clicks'].max()), [int(data['Clicks'].min()), int(data['Clicks'].max())])
        data = data[(data['Clicks'] >= min_clicks) & (data['Clicks'] <= max_clicks)]

        # Filter by Impressions
        min_impressions, max_impressions = st.sidebar.slider('Impressions', int(data['Impressions'].min()), int(data['Impressions'].max()), [int(data['Impressions'].min()), int(data['Impressions'].max())])
        data = data[(data['Impressions'] >= min_impressions) & (data['Impressions'] <= max_impressions)]

        # Filter by CTR
        min_ctr, max_ctr = st.sidebar.slider('CTR', float(data['CTR'].min()), float(data['CTR'].max()), [float(data['CTR'].min()), float(data['CTR'].max())])
        data = data[(data['CTR'] >= min_ctr) & (data['CTR'] <= max_ctr)]

        # Filter by Position
        min_position, max_position = st.sidebar.slider('Position', float(data['Position'].min()), float(data['Position'].max()), [float(data['Position'].min()), float(data['Position'].max())])
        data = data[(data['Position'] >= min_position) & (data['Position'] <= max_position)]

        # Display the filtered data
        st.write(data)

if __name__ == '__main__':
    main()
