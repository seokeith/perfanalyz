import pandas as pd
import streamlit as st

def calculate_performance(df, analyze_by):
    if analyze_by == 'Full URL':
        avg_df = df.groupby('URL').mean().reset_index()
    elif analyze_by == 'Individual Queries':
        avg_df = df.groupby(['URL', 'queries']).mean().reset_index()

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

        st.subheader('Uploaded Data:')
        st.write(data)

        col_input = st.text_input("Enter the column names (comma-separated)", "month,URL,queries,impressions,clicks,average position,click through rate")
        columns = [col.strip() for col in col_input.split(',')]

        if all(col in data.columns for col in columns):
            analyze_by = st.radio("Choose how to analyze performance:", ("Full URL", "Individual Queries"))

            # Perform the performance analysis for URLs and queries
            result = calculate_performance(data[columns], analyze_by)

            st.subheader('Performance Analysis:')
            st.write(result)
        else:
            st.warning("One or more of the specified columns is not in the dataset.")

if __name__ == '__main__':
    main()
