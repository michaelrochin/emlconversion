import os
import re
from tika import parser

# Directory containing your .eml files
input_dir = "bernth1"
output_dir = "responses_only"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".eml"):
        file_path = os.path.join(input_dir, filename)

        # Parse the email content
        parsed = parser.from_file(file_path)
        email_content = parsed.get("content", "")

        # Regex to extract user response (basic examples, adjust as needed)
        match = re.search(r"(?<=Re:).*?(?=\nSent from|\nOn \w+|$)", email_content, re.S | re.I)

        if match:
            response = match.group(0).strip()
        else:
            response = "No clear response found."

        # Sanitize filename for the output file
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', filename.replace(".eml", ".txt"))

        # Write response to output file
        output_path = os.path.join(output_dir, sanitized_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response)

print("Responses extracted and saved in:", output_dir)
