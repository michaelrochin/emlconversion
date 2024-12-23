import os
import re
from tika import parser
import streamlit as st
import matplotlib.pyplot as plt

# Function to parse .eml file and extract response
def extract_responses(file):
    parsed = parser.from_file(file)
    email_content = parsed.get("content", "")

    # Regex to extract user response
    match = re.search(r"(?<=Re:).*?(?=\nSent from|\nOn \w+|$)", email_content, re.S | re.I)

    if match:
        return match.group(0).strip()
    return "No clear response found."

# Main Streamlit App
def main():
    st.title("EML File Converter & Word Cloud Generator")

    # File Uploader
    uploaded_files = st.file_uploader("Upload your .eml files", type=["eml"], accept_multiple_files=True)

    if uploaded_files:
        responses = []

        # Process each uploaded file
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract response
            response = extract_responses(uploaded_file.name)
            responses.append(response)

        # Display extracted responses
        st.subheader("Extracted Responses")
        for idx, response in enumerate(responses, start=1):
            st.write(f"**Response {idx}:** {response}")

        # Create Word Cloud
        if responses:
            st.subheader("Word Cloud")
            text_corpus = " ".join(responses)
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_corpus)

            # Display Word Cloud
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

# Run the app
if __name__ == "__main__":
    main()
