from tika import parser
import streamlit as st
import re
from io import StringIO

def extract_responses(file):
    """Extract responses from an uploaded .eml file."""
    # Parse the file content
    parsed = parser.from_buffer(file.read())
    email_content = parsed.get("content", "")

    # Regex to extract user responses
    match = re.search(r"(?<=Re:).*?(?=\nSent from|\nOn \w+|$)", email_content, re.S | re.I)

    if match:
        return match.group(0).strip()
    else:
        return "No clear response found."

def main():
    st.title("EML File Converter & Word Cloud Generator")
    st.write("Upload your .eml files")

    # File uploader
    uploaded_files = st.file_uploader("Drag and drop files here", accept_multiple_files=True, type=["eml"])

    if uploaded_files:
        st.write("Processing uploaded files...")
        responses = []

        for uploaded_file in uploaded_files:
            response = extract_responses(uploaded_file)
            responses.append((uploaded_file.name, response))

        # Display results
        for file_name, response in responses:
            st.subheader(f"Response from {file_name}")
            st.text(response)

        # Combine all responses for word cloud
        all_responses = " ".join([resp for _, resp in responses])
        generate_wordcloud(all_responses)

def generate_wordcloud(text):
    """Generate and display a word cloud."""
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    st.subheader("Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
