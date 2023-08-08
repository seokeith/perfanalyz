import streamlit as st
import pandas as pd

def validate_data(data):
    # Check URL column for string format
    if not all(isinstance(item, str) for item in data['URL']):
        return 'URL column should only contain strings representing the web URL.'

    # Check Clicks column for integer format
    if not all(isinstance(item, (int, float)) and item.is_integer() for item in data['Clicks']):
        return 'Clicks column should only contain integers representing the number of clicks.'

    # Check Impressions column for integer format
    if not all(isinstance(item, (int, float)) and item.is_integer() for item in data['Impressions']):
        return 'Impressions column should only contain integers representing the number of impressions.'

    # Check CTR column for float format between 0.0 and 1.0
    if not all(isinstance(item, float) and 0.0 <= item <= 1.0 for item in data['CTR']):
        return 'CTR column should only contain floats between 0.0 and 1.0 representing the Click Through Rate.'

    # Check Position column for float format
    if not all(isinstance(item, float) for item in data['Position']):
        return 'Position column should only contain floats representing the rank or position of the URL.'

    return None  # If all validations pass

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

        # Perform additional validation on data columns
        validation_message = validate_data(data)
        if validation_message:
            st.error(validation_message)
            return

        # Display the URLs and entire data
        st.write(data['URL'])
        st.write(data)

if __name__ == '__main__':
    main()
