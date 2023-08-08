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
                
                # URL multi-select dropdown filter in the sidebar
                selected_urls = st.sidebar.multiselect(
                    'Select URLs:',
                    options=list(data['URL'].unique()),
                    default=list(data['URL'].unique())
                )

                # If specific URLs are selected, filter the data by the selected URLs
                if selected_urls:
                    data = data[data['URL'].isin(selected_urls)]
                
                # Slider for filtering by number of clicks
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

                # Slider for filtering by number of impressions
                min_impressions = int(data['Impressions'].min())
                max_impressions = int(data['Impressions'].max())

                if min_impressions != max_impressions:
                    impressions_range = st.sidebar.slider(
                        "Filter by number of impressions:",
                        min_impressions,
                        max_impressions,
                        (min_impressions, max_impressions)
                    )
                else:
                    impressions_range = (min_impressions, max_impressions)
                    st.sidebar.text(f"Only one value for impressions: {min_impressions}")

                # Slider for filtering by CTR
                min_ctr = float(data['CTR'].min())
                max_ctr = float(data['CTR'].max())

                if min_ctr != max_ctr:
                    ctr_range = st.sidebar.slider(
                        "Filter by CTR:",
                        min_ctr,
                        max_ctr,
                        (min_ctr, max_ctr)
                    )
                else:
                    ctr_range = (min_ctr, max_ctr)
                    st.sidebar.text(f"Only one value for CTR: {min_ctr:.2f}")

                # Calculate the average clicks, impressions, and CTR
                avg_clicks = data['Clicks'].mean()
                st.sidebar.text(f"Average Clicks: {avg_clicks:.2f}")
                avg_impressions = data['Impressions'].mean()
                st.sidebar.text(f"Average Impressions: {avg_impressions:.2f}")
                avg_ctr = data['CTR'].mean()
                st.sidebar.text(f"Average CTR: {avg_ctr:.2f}%")

                # Button to show URLs with lower than average values
                if st.sidebar.button("Show URLs with less than average clicks"):
                    lower_than_avg_clicks = data[data['Clicks'] < avg_clicks]
                    sorted_clicks = lower_than_avg_clicks.sort_values(by='Clicks', ascending=True)
                    for index, row in sorted_clicks.iterrows():
                        st.write(row['URL'], "-", row['Clicks'], "clicks", "-", row['Impressions'], "impressions", "-", row['CTR'], "CTR", "-", row['Position'], "position")
                elif st.sidebar.button("Show URLs with less than average impressions"):
                    lower_than_avg_impressions = data[data['Impressions'] < avg_impressions]
                    sorted_impressions = lower_than_avg_impressions.sort_values(by='Impressions', ascending=True)
                    for index, row in sorted_impressions.iterrows():
                        st.write(row['URL'], "-", row['Clicks'], "clicks", "-", row['Impressions'], "impressions", "-", row['CTR'], "CTR", "-", row['Position'], "position")
                elif st.sidebar.button("Show URLs with less than average CTR"):
                    lower_than_avg_ctr = data[data['CTR'] < avg_ctr]
                    sorted_ctr = lower_than_avg_ctr.sort_values(by='CTR', ascending=True)
                    for index, row in sorted_ctr.iterrows():
                        st.write(row['URL'], "-", row['Clicks'], "clicks", "-", row['Impressions'], "impressions", "-", row['CTR'], "CTR", "-", row['Position'], "position")
                else:
                    filtered_data = data[(data['Clicks'] >= clicks_range[0]) & (data['Clicks'] <= clicks_range[1]) & 
                                         (data['Impressions'] >= impressions_range[0]) & (data['Impressions'] <= impressions_range[1]) & 
                                         (data['CTR'] >= ctr_range[0]) & (data['CTR'] <= ctr_range[1])]

                    for index, row in filtered_data.iterrows():
                        st.write(row['URL'], "-", row['Clicks'], "clicks", "-", row['Impressions'], "impressions", "-", row['CTR'], "CTR", "-", row['Position'], "position")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
