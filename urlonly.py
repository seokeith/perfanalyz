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
                
                # Reset Filters Button
                if st.sidebar.button("Reset Filters"):
                    st.experimental_rerun()
                
                # URL multi-select dropdown filter in the sidebar
                selected_urls = st.sidebar.multiselect(
                    'Select URLs:',
                    options=list(data['URL'].unique()),
                    default=list(data['URL'].unique())
                )

                # If specific URLs are selected, filter the data by the selected URLs
                if selected_urls:
                    data = data[data['URL'].isin(selected_urls)]
                
                # Slider for filtering by number of clicks, impressions, CTR, and position
                attributes_ranges = {
                    'Clicks': [int(data['Clicks'].min()), int(data['Clicks'].max())],
                    'Impressions': [int(data['Impressions'].min()), int(data['Impressions'].max())],
                    'CTR': [float(data['CTR'].min()), float(data['CTR'].max())],
                    'Position': [float(data['Position'].min()), float(data['Position'].max())]
                }

                selected_ranges = {}
                for attr, (min_val, max_val) in attributes_ranges.items():
                    if min_val != max_val:
                        selected_ranges[attr] = st.sidebar.slider(
                            f"Filter by {attr.lower()}:",
                            min_val, max_val, (min_val, max_val)
                        )
                    else:
                        selected_ranges[attr] = (min_val, max_val)
                        st.sidebar.text(f"Only one value for {attr.lower()}: {min_val}")

                # Calculate the average clicks, impressions, CTR, and position
                averages = {
                    'Clicks': data['Clicks'].mean(),
                    'Impressions': data['Impressions'].mean(),
                    'CTR': data['CTR'].mean(),
                    'Position': data['Position'].mean()
                }
                for attr, avg_val in averages.items():
                    st.sidebar.text(f"Average {attr}: {avg_val:.2f}")

                # Button to show URLs with lower or higher than average values (higher for Position)
                display_data = None
                for attr, avg_val in averages.items():
                    if st.sidebar.button(f"Show URLs with {'higher' if attr == 'Position' else 'less'} than average {attr.lower()}"):
                        if attr == 'Position':
                            display_data = data[data[attr] > avg_val]
                        else:
                            display_data = data[data[attr] < avg_val]
                        display_data = display_data.sort_values(by=attr, ascending=(attr == 'Position'))
                        break

                if display_data is None:
                    display_data = data
                    for attr, (min_val, max_val) in selected_ranges.items():
                        display_data = display_data[(display_data[attr] >= min_val) & (display_data[attr] <= max_val)]

                for index, row in display_data.iterrows():
                    st.write(row['URL'], "-", row['Clicks'], "clicks", "-", row['Impressions'], "impressions", "-", row['CTR'], "CTR", "-", row['Position'], "position")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
