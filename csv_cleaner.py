import streamlit as st
import pandas as pd
import io
import os
from firebase_admin import credentials, auth
import firebase_admin

# Get Firebase key from Render secret
firebase_key = os.environ.get('FIREBASE_KEY')
if not firebase_key:
    st.error("Firebase key not found. Check Render secrets.")
else:
    # Convert the JSON string to a credential object
    import json
    cred = credentials.Certificate(json.loads(firebase_key))
    firebase_admin.initialize_app(cred)

def authenticate_user():
    if 'user' not in st.session_state:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.user = user.email
                st.success("Logged in as {}".format(user.email))
            except auth.AuthError:
                st.error("Invalid credentials")
        if st.button("Sign Up"):
            try:
                auth.create_user(email=email, password=password)
                st.success("Account created! Please log in.")
            except:
                st.error("Error creating account")
    return 'user' in st.session_state

if authenticate_user():
    st.title("Cloud-Based CSV Cleaner")
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Original Data")
        st.dataframe(df.head())
        if st.checkbox("Remove duplicates"):
            df = df.drop_duplicates()
        if st.selectbox("Missing values", ["None", "Drop", "Fill mean"]) == "Drop":
            df = df.dropna()
        elif st.selectbox("Missing values", ["None", "Drop", "Fill mean"]) == "Fill mean":
            df = df.fillna(df.mean())
        st.subheader("Cleaned Data")
        st.dataframe(df.head())
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button("Download CSV", csv_buffer.getvalue(), "cleaned_data.csv")
else:
    st.write("Please log in or sign up.")