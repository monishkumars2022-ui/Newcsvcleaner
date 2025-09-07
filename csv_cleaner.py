import pandas as pd
import streamlit as st
import io

st.title("Cloud-Based CSV Cleaner")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        st.subheader("Original Data Preview")
        st.dataframe(df.head())

        # Cleaning options
        st.subheader("Cleaning Options")
        remove_duplicates = st.checkbox("Remove duplicates")
        handle_missing = st.selectbox("Handle missing values", ["None", "Drop rows", "Fill with mean"])

        # Apply cleaning
        if remove_duplicates:
            df = df.drop_duplicates()
            st.write(f"Removed {df.duplicated().sum()} duplicate rows.")

        if handle_missing == "Drop rows":
            before = len(df)
            df = df.dropna()
            st.write(f"Dropped {before - len(df)} rows with missing values.")
        elif handle_missing == "Fill with mean":
            numeric_cols = df.select_dtypes(include=['number']).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("Filled missing numeric values with column means.")

        # Display cleaned data
        st.subheader("Cleaned Data Preview")
        st.dataframe(df.head())

        # Download cleaned CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Cleaned CSV",
            data=csv_buffer.getvalue(),
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")