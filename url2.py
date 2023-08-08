import pandas as pd
import streamlit as st

def calculate_performance(df, analyze_by):
    if analyze_by == 'Full URL':
        # Calculate average values for each URL
        avg_df = df.groupby('URL').agg({
            'impressions': 'mean',
            'clicks': 'mean',
            'average position': 'mean',
            'click through rate': 'mean'
        }).reset_index()
    elif analyze_by == 'Individual Queries':
        # Calculate average values for each URL and query
        avg_df = df.groupby(['URL', 'queries']).agg({
            'impressions': 'mean',
            'clicks': 'mean',
            'average position': 'mean',
            'click through rate': 'mean'
        }).reset_index()

    # Calculate performance compared to the overall average values
    overall_avg = df[['impressions', 'clicks', 'average position', 'click through rate']].mean()
    performance_df = avg_df.copy()
    for metric in ['impressions', 'clicks', 'average position', 'click through rate']:
        performance_df[f'{metric} performance'] = performance_df[metric] / overall_avg[metric]

    return performance_df

# Streamlit app code
def main():
    st.title('URL and Query Performance Analysis')

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error: {e}")
            st.write("Please ensure your CSV file is correctly formatted.")
            return

        if 'queries' not in data.columns:
            st.warning("The 'queries' column is missing in the CSV file.")
            return

        # Show the uploaded data
        st.subheader('Uploaded Data:')
        st.write(data)

        # Ask user how to analyze the performance
        analyze_by = st.radio("Choose how to analyze performance:", ("Full URL", "Individual Queries"))

        # Perform the performance analysis for URLs and queries
        result = calculate_performance(data, analyze_by)

        # Display the result
        st.subheader('Performance Analysis:')
        st.write(result)

if __name__ == '__main__':
    main()
