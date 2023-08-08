import streamlit as st
import pandas as pd

def main():
    st.title('CSV Data Viewer')

    st.write("""
    Directions:
    - The CSV should have the following columns: URL, Clicks, Impressions, CTR, and Position.
    - URL: Should be a string representing the web URL.
    - Clicks: Should be an integer representing the number of clicks.
    - Impressions: Should be an integer representing the number of impressions.
    - CTR: Should be a float (0.0 to 1.0) representing the Click Through Rate.
    - Position: Should be a float representing the rank or position of the URL.
    """)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f'Error reading CSV: {e}')
            return

        # Validate the CSV format
        expected_columns = ["URL", "Clicks", "Impressions", "CTR", "Position"]
        if not all(col in data.columns for col in expected_columns):
            st.error('Invalid CSV file format. Please make sure the CSV has the required columns.')
            return
        
        # Display the URLs
        st.write(data['URL'])
        
        # Display the entire data
        st.write(data)

if __name__ == '__main__':
    main()
