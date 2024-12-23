import re
from tika import parser
import streamlit as st


def extract_responses(file):
    """
    Extracts the meaningful responses from the .eml file content.
    """
    parsed = parser.from_buffer(file)
    email_content = parsed.get("content", "")
    
    # Use regex to clean and extract user responses
    match = re.search(r"(?<=Re:).*?(?=\nSent from|\nOn \w+|$)", email_content, re.S | re.I)
    if match:
        response = match.group(0).strip()
    else:
        response = "No clear response found."

    # Remove unwanted characters
    response = re.sub(r'[^\x20-\x7E\n]', '', response)
    return response


def save_to_txt(file_name, content):
    """
    Saves the extracted content to a .txt file.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    st.title("EML File Converter & Response Extractor")
    st.write("Upload your `.eml` files to extract responses and save them as `.txt`.")

    uploaded_files = st.file_uploader(
        "Upload .eml files", type="eml", accept_multiple_files=True
    )

    if uploaded_files:
        st.write("Processing files...")

        for uploaded_file in uploaded_files:
            # Extract meaningful response
            response = extract_responses(uploaded_file)

            # Display results in the app
            st.subheader(f"Extraction Results for {uploaded_file.name}")
            st.text_area(f"Response from {uploaded_file.name}", response)

            # Save to a .txt file
            txt_file_name = uploaded_file.name.replace(".eml", ".txt")
            save_to_txt(txt_file_name, response)

            st.success(f"Saved to: {txt_file_name}")

        st.success("All files processed successfully!")


if __name__ == "__main__":
    main()
