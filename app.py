import os
import re
from tika import parser
import streamlit as st
import tempfile

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
            # Use a temporary file for Tika processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".eml") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name
            
            try:
                response = extract_responses(temp_file_path)
                st.write(f"**{uploaded_file.name}**")
                st.text_area("Response:", value=response, height=150)
            except Exception as e:
                st.error(f"Failed to process file {uploaded_file.name}: {str(e)}")
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)

# Run the app
if __name__ == "__main__":
    main()
