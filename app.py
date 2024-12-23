import streamlit as st
from tika import parser
import os
import re

# Configure Tika server to use local JAR file
os.environ['TIKA_SERVER_JAR'] = r"E:\Projects\Word Clous\Tika\tika-app-3.0.0.jar"

# Function to process EML files
def process_eml_file(file_path):
    parsed = parser.from_file(file_path)
    content = parsed.get('content', '').strip()
    return content

# Streamlit interface
st.title("EML Response Extractor")
uploaded_file = st.file_uploader("Upload EML files", type=["eml"])

if uploaded_file is not None:
    st.write("Processing files...")
    try:
        # Save uploaded file temporarily
        with open(uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.read())

        # Process the uploaded file
        response = process_eml_file(uploaded_file.name)
        if response:
            st.text_area("Extracted Content", response, height=300)
        else:
            st.write("No content found in the file.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
