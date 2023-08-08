import streamlit as st
import pandas as pd

# Function to calculate the page performance and compare against expected values
def calculate_performance(df, expected_clickout_rate, expected_ftd_rate, expected_rev_per_ftd):
    df['Expected_Clickouts'] = df['Users'] * expected_clickout_rate
    df['Expected_FTDs'] = df['Expected_Clickouts'] * expected_ftd_rate
    df['Expected_Revenue'] = df['Expected_FTDs'] * expected_rev_per_ftd
    df['Difference'] = df['Revenue'] - df['Expected_Revenue']
    df['Performance'] = df.apply(lambda row: 'Overperforming' if row['Difference'] > 0 else 'Underperforming', axis=1)
    return df

# Streamlit app code
def main():
    st.title('Page Performance Analysis')
    
    # Instructions
    st.write("Upload a CSV file containing the following columns:")
    st.write("- URL")
    st.write("- Users")
    st.write("- Clickouts")
    st.write("- FTD")
    st.write("- Conversion Rate")
    st.write("- Revenue")
    st.write("Ensure the column names are spelled exactly as listed above.")

    # File upload and data input
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        st.subheader('Input expected rates:')
        expected_clickout_rate = st.number_input('Expected Clickout rate from users', min_value=0.0, step=0.01, value=0.1, format="%.2f")
        expected_ftd_rate = st.number_input('Expected FTD rate from clickouts', min_value=0.0, step=0.01, value=0.3, format="%.2f")
        expected_rev_per_ftd = st.number_input('Expected Revenue per FTD', min_value=0.0, step=0.01, value=100.0, format="%.2f")

        if st.button('Calculate'):
            df_result = calculate_performance(df, expected_clickout_rate, expected_ftd_rate, expected_rev_per_ftd)
            st.dataframe(df_result)

# Run the app
if __name__ == "__main__":
    main()
