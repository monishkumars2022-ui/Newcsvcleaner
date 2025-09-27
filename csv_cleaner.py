import streamlit as st
import pandas as pd
import io
from firebase_admin import credentials, auth
import firebase_admin

# Initialize Firebase with local service account key
try:
    print("Attempting to load serviceAccountKey.json...")
    with open('D:\Csv Cleaner with auth/serviceAccountKey.json', 'r') as f:
        data = f.read()
        print("File content loaded successfully.")
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully.")
except FileNotFoundError as e:
    st.error(f"serviceAccountKey.json not found: {e}")
    st.stop()
except ValueError as e:
    st.error(f"Invalid service account key: {e}")
    st.stop()
except Exception as e:
    st.error(f"Unexpected error initializing Firebase: {e}")
    st.stop()

# Authentication function
def authenticate_user():
    if 'user' not in st.session_state:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.user = user.email
                st.success(f"Logged in as {user.email}")
            except auth.AuthError as e:
                st.error(f"Invalid credentials: {e}")
        if st.button("Sign Up"):
            try:
                auth.create_user(email=email, password=password)
                st.success("Account created! Please log in.")
            except Exception as e:
                st.error(f"Error creating account: {e}")
    return 'user' in st.session_state

# Main app logic
if authenticate_user():
    st.title("Cloud-Based CSV Cleaner")
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Original Data")
        st.dataframe(df.head())

        # Cleaning options
        if st.checkbox("Remove duplicates"):
            df = df.drop_duplicates()
        if st.selectbox("Missing values", ["None", "Drop", "Fill mean"]) == "Drop":
            df = df.dropna()
        elif st.selectbox("Missing values", ["None", "Drop", "Fill mean"]) == "Fill mean":
            df = df.fillna(df.mean())

        st.subheader("Cleaned Data")
        st.dataframe(df.head())

        # Download cleaned CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button("Download CSV", csv_buffer.getvalue(), "cleaned_data.csv")
else:
    st.write("Please log in or sign up.")