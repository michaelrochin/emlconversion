import os
import re
from tika import parser
import streamlit as st

# Function to extract response from email content
def extract_response(email_content):
    match = re.search(r"(?<=Re:).*?(?=\nSent from|\nOn \w+|$)", email_content, re.S | re.I)
    if match:
        return match.group(0).strip()
    return "No clear response found."

# Streamlit App
st.title("EML File Response Extractor")
st.write("Upload your `.eml` files to extract responses.")

# File uploader for multiple files
uploaded_files = st.file_uploader("Upload .eml files", type=["eml"], accept_multiple_files=True)

if uploaded_files:
    st.write("Processing files...")

    for uploaded_file in uploaded_files:
        # Parse the email content using Tika
        email_content = uploaded_file.read().decode("utf-8")  # Decode the uploaded file
        parsed = parser.from_buffer(email_content)
        extracted_text = parsed.get("content", "")

        # Extract the response using regex
        response = extract_response(extracted_text)

        # Display results on the page
        st.subheader(f"Response from {uploaded_file.name}:")
        st.text(response)

st.write("Upload more files to process their responses!")
