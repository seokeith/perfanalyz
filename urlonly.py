import streamlit as st
import pandas as pd

def find_lowest_performing_urls(df, num_urls=10):
    url_averages = df.groupby('URL').mean().reset_index()
    lowest_performing_urls = url_averages.nsmallest(num_urls, 'Clicks')
    return lowest_performing_urls

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

        lowest_performing_urls = find_lowest_performing_urls(df)
        st.subheader('Top 10 Lowest Performing URLs:')
        st.write(lowest_performing_urls)

if __name__ == '__main__':
    main()
