import os
import re
from tika import parser
import streamlit as st

# Function to parse .eml file and extract responses
def extract_responses(file):
    """Extract response content from an .eml file."""
    parsed = parser.from_file(file)
    email_content = parsed.get("content", "")

    # Regex to extract user response (adjust as needed)
    match = re.search(r"(?<=Re:).*?(?=\nSent from|\nOn \w+|$)", email_content, re.S | re.I)
    if match:
        response = match.group(0).strip()
    else:
        response = "No clear response found."
    return response

# Main Streamlit app
def main():
    st.title("EML File Converter")
    st.write("Upload your .eml files, and I'll extract the responses!")

    uploaded_files = st.file_uploader("Upload .eml files", accept_multiple_files=True, type="eml")

    if uploaded_files:
        st.subheader("Extraction Results")
        for uploaded_file in uploaded_files:
            response = extract_responses(uploaded_file.name)
            st.write(f"**{uploaded_file.name}**")
            st.text_area("Response:", value=response, height=150)

# Run the app
if __name__ == "__main__":
    main()
