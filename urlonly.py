import streamlit as st
import pandas as pd

def calculate_click_comparison(df):
    # Group by average rank and calculate mean clicks
    avg_rank_clicks = df.groupby('Average rank')['Clicks'].mean().reset_index()

    # Group by impressions and calculate mean clicks
    impressions_clicks = df.groupby('Impressions')['Clicks'].mean().reset_index()

    return avg_rank_clicks, impressions_clicks

def main():
    st.title('URL Metrics Analysis')

    # File Upload
    st.write('Upload a CSV file with columns: URLs, Clicks, Impressions, Average Rank, Click Through Rate')
    uploaded_file = st.file_uploader('Choose a CSV file', type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Show the uploaded data
        st.subheader('Uploaded Data:')
        st.dataframe(df)

        # Calculate click comparisons
        avg_rank_clicks, impressions_clicks = calculate_click_comparison(df)

        # Show click comparisons based on average rank
        st.subheader('Clicks Comparison based on Average Rank:')
        st.dataframe(avg_rank_clicks)

        # Show click comparisons based on impressions
        st.subheader('Clicks Comparison based on Impressions:')
        st.dataframe(impressions_clicks)

if __name__ == '__main__':
    main()
