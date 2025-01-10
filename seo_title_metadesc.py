import streamlit as st
import pandas as pd
import io

# Streamlit app title
st.title("Load and Enhance Excel File with Variations")

# Editable variables with placeholders
language = st.text_input("Enter Language:", value="Danish", placeholder="e.g., Danish")
discount = st.text_input("Enter Discount:", value="20%", placeholder="e.g., 20%")
amount = st.text_input("Enter Amount:", value="€50", placeholder="e.g., €50")

# Display the current values of the variables
st.write("### Editable Variables")
st.write(f"**Language:** {language}")
st.write(f"**Discount:** {discount}")
st.write(f"**Amount:** {amount}")

# File uploader for Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read the "real" sheet into a DataFrame
        property_count = pd.read_excel(uploaded_file, sheet_name="real")
        
        if isinstance(property_count, pd.DataFrame):
            st.success("Property Count is successfully loaded as a DataFrame.")

            # Check for required columns
            if 'Suffix' in property_count.columns and 'Count' in property_count.columns:
                # Create 'region' column
                property_count['region'] = property_count['Suffix'].apply(
                    lambda x: x.strip('/').split('/')[-1].capitalize()
                )

                # Create variation1 column
                property_count['variation1'] = property_count.apply(
                    lambda row: (
                        f"Meta Title: {row['Count']} Holiday Homes in {row['region']} - Discover Nature’s Wonders\n"
                        f"Meta Description: Take a vacation in {row['region']}! Rent a holiday home and experience stunning landscapes, fjords, and cozy cabins.\n"
                        f"H1: Discover {row['region']} - Rent a Holiday Home in Beautiful Nature"
                    ),
                    axis=1
                )

                # Create variation2 column
                property_count['variation2'] = property_count.apply(
                    lambda row: (
                        f"Meta Title: Looking for Vacation in {row['region']}? Rent a Holiday Home Now!\n"
                        f"Meta Description: Explore {row['region']}’s fantastic nature from your own holiday home. "
                        f"Find the perfect spot for your next vacation here!\n"
                        f"H1: Rent a Holiday Home in {row['region']} - Your Vacation Awaits"
                    ),
                    axis=1
                )

                # Create variation3 column
                property_count['variation3'] = property_count.apply(
                    lambda row: (
                        f"Meta Title: Rent a Holiday Home in {row['region']} – Save upto {discount} on Your Booking\n"
                        f"Meta Description: Find {row['Count']} unique holiday homes in {row['region']} and enjoy magnificent nature. "
                        f"Perfect for family vacations or adventures with friends. Book now and save {amount}!\n"
                        f"H1: Your Dream Vacation in {row['region']} – Rent a Holiday Home Now"
                    ),
                    axis=1
                )

                st.success("Variations successfully added to the DataFrame.")
                st.write("Updated Property Count DataFrame:")
                st.dataframe(property_count)

                # Provide a download button for the updated DataFrame
                @st.cache_data
                def convert_df_to_excel(df):
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name="Updated Data")
                        writer.save()
                    buffer.seek(0)
                    return buffer

                excel_data = convert_df_to_excel(property_count)
                st.download_button(
                    label="Download Updated Data as Excel",
                    data=excel_data,
                    file_name="updated_property_count.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Required columns 'Suffix' and 'Count' are missing in the uploaded file.")
        else:
            st.error("Error: Property Count is not a DataFrame.")
    except Exception as e:
        st.error(f"An error occurred while reading or processing the file: {e}")
else:
    st.info("Please upload an Excel file to proceed.")
