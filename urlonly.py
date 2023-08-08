import streamlit as st
import pandas as pd

def calculate_click_comparison(df):
    avg_position_clicks = df.groupby('Average Position')['Clicks'].mean().reset_index()
    impressions_clicks = df.groupby('Impressions')['Clicks'].mean().reset_index()
    return avg_position_clicks, impressions_clicks

def main():
    st.title('URL Metrics Analysis')
    
    st.sidebar.write('Upload a CSV file with the following columns:')
    st.sidebar.write('- URL')
    st.sidebar.write('- Clicks')
    st.sidebar.write('- Impressions')
    st.sidebar.write('- CTR')
    st.sidebar.write('- Average Position')

    uploaded_file = st.sidebar.file_uploader('Choose a CSV file', type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.subheader('Uploaded Data:')
        st.write(df)

        avg_position_clicks, impressions_clicks = calculate_click_comparison(df)

        st.subheader('Clicks Comparison based on Average Position:')
        st.write(avg_position_clicks)

        st.subheader('Clicks Comparison based on Impressions:')
        st.write(impressions_clicks)

if __name__ == '__main__':
    main()
