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
    st.title("URL Data Analysis")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            
            # Dropdown filter for URL
            selected_url = st.sidebar.selectbox(
                "Filter by URL:", 
                options=data['URL'].unique(), 
                index=0
            )
            data = data[data['URL'] == selected_url]
            
            # Slider in the sidebar for filtering by number of clicks
            min_clicks = int(data['Clicks'].min())
            max_clicks = int(data['Clicks'].max())
            if min_clicks == max_clicks:
                st.sidebar.text(f"Clicks: {min_clicks}")
                clicks_range = (min_clicks, max_clicks)
            else:
                clicks_range = st.sidebar.slider(
                    "Filter by number of clicks:",
                    min_clicks,
                    max_clicks,
                    (min_clicks, max_clicks)
                )
            
            # Filter data by selected range of clicks
            data = data[(data['Clicks'] >= clicks_range[0]) & (data['Clicks'] <= clicks_range[1])]
            
            # Calculate average clicks and show URLs with below-average clicks
            avg_clicks = data['Clicks'].mean()
            st.sidebar.text(f"Average Clicks: {avg_clicks:.2f}")
            below_avg_data = data[data['Clicks'] < avg_clicks]
            st.sidebar.text("URLs with below average clicks:")
            st.sidebar.write(below_avg_data.sort_values(by="Clicks")[['URL', 'Clicks']])
            
            # Display the filtered data
            st.write(data[['URL', 'Clicks']])
            
        except Exception as e:
            st.write("There was an error loading the data. Please ensure the file is in the correct format.")
            st.write("Details:", e)

if __name__ == "__main__":
    main()

