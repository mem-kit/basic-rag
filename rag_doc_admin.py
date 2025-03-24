import os, logging
import streamlit as st
from pathlib import Path

from rag.rag_index_builder import RAGBuildIndex

##
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if "build_index" not in st.session_state:
    st.session_state.build_index = False

if "building" not in st.session_state:
    st.session_state.building = False

# Define the folder to manage
DIRECTORY = "./rag/data_docs"
# Ensure the directory exists
Path(DIRECTORY).mkdir(parents=True, exist_ok=True)


# List files
files = os.listdir(DIRECTORY)
files = [f for f in files if os.path.isfile(os.path.join(DIRECTORY, f))]

st.subheader("Files in Knowledge Base")
if files:
    for file in files:
        file_path = os.path.join(DIRECTORY, file)
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write(file)

        # Download button
        with open(file_path, "rb") as f:
            col4.download_button(label="Download", data=f, file_name=file)

        # Delete button
        if col5.button("Delete", key=file):
            os.remove(file_path)
            st.rerun(scope="app")

else:
    st.write("No files found.")

# Upload files
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    save_path = os.path.join(DIRECTORY, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    st.rerun(scope="app")


with st.sidebar:
    for it in range(0, 13):
        st.write("\n")
    st.markdown("---")

    st.write(":red[Do Not Trigger it], If you are not the knowledge base manager!")
    if not st.session_state.building:
        if st.button("Build Index"):
            st.warning("Do you want to rebuild the index for documents? It may take a long time.")
            logger.info("click build")
            st.session_state.build_index = True

        if st.session_state.build_index:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Build"):
                    logger.info("build: yes")
                    st.session_state.building = True
                    st.session_state.build_index = False
                    st.rerun(scope="app")
            with col2:
                if st.button("Cancel"):
                    logger.info("build: no")
                    st.session_state.build_index = False
                    st.rerun(scope="app")


    if st.session_state.building:
        logger.info("building...")
        st.info("Building Index...")
        RAGBuildIndex.build()
        st.success("Build Index Completed, Please Check Log in the Server.")
        st.session_state.building = False
        st.rerun(scope="app")

