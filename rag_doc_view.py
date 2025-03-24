
import streamlit as st
import os, docx2txt, logging
from PyPDF2 import PdfReader
from io import BytesIO

##
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

st.subheader("", divider="red")

# Specify the directory you want to list
directory = "./rag/data_docs"
files = list_files_in_directory(directory)

# Create two columns
col1, col2 = st.columns([1, 3])

with col1:
    selected_file = st.selectbox("Choose a file", files)

# Check if a file is selected
if selected_file:
    # Construct the file path
    file_path = os.path.join(directory, selected_file)

    # Read the file contents
    with open(file_path, "rb") as file:
        file_bytes = file.read()

    # Display file content in the right column
    with col2:
        if selected_file:
            # Show file contents
            file_path = os.path.join(directory, selected_file)
            logger.info(f"select file: {file_path}")
            with open(file_path, "rb") as file:
                file_bytes = file.read()

            # Display file content
            if selected_file.lower().endswith('.pdf'):
                pdf_reader = PdfReader(BytesIO(file_bytes))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                st.text_area("Preview PDF Content", text, height=300)

            elif selected_file.lower().endswith('.txt'):
                st.text_area("Text File Content", file_bytes.decode('utf-8'), height=300)

            elif selected_file.lower().endswith('.docx'):
                text = docx2txt.process(BytesIO(file_bytes))
                st.text_area("Word File Content", text, height=300)

            # Download file
            st.download_button(
                label="Download file",
                data=file_bytes,
                file_name=selected_file
            )
