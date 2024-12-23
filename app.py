import os
import re
from tika import parser
import streamlit as st

# Function to parse .eml file and extract response
def extract_responses(file):
    parsed = parser.from_file(file)
    email_content = parsed.get("content", "")
    
    # Regex to extract user response (customize as needed)
    match = re.search(r"(?<=Re:).*?(?=\nSent from|\nOn \w+|$)", email_content, re.S | re.I)
    if match:
        return match.group(0).strip()
    return ""

# Main function for Streamlit app
def main():
    st.title("EML File Converter & Combined Text Generator")
    st.subheader("Upload your .eml files")

    uploaded_files = st.file_uploader(
        "Drag and drop files here",
        type=["eml"],
        accept_multiple_files=True
    )

    if st.button("Process Files"):
        if uploaded_files:
            combined_text = ""
            for uploaded_file in uploaded_files:
                # Extract response from each file
                response = extract_responses(uploaded_file)
                combined_text += response + "\n\n"

            # Save combined text to a file
            combined_file_name = "combined_output.txt"
            with open(combined_file_name, "w", encoding="utf-8") as f:
                f.write(combined_text)

            st.success("All files processed successfully!")
            st.download_button(
                label="Download Combined Text",
                data=combined_text,
                file_name="combined_output.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please upload at least one file.")

if __name__ == "__main__":
    main()
